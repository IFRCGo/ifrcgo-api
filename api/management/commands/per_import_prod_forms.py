import csv
from django.db import transaction
from django.core.management.base import BaseCommand
from per.models import Overview, AssessmentType, Form, FormData, FormArea, FormComponent, FormQuestion, FormAnswer


class Command(BaseCommand):
    help = 'Imports Overviews, Forms, FormData deleted from production'
    missing_args_message = "overviews_filename (1st arg), forms_filename (2nd arg) or formdata_filename (3rd arg) are missing"

    def add_arguments(self, parser):
        parser.add_argument('overviews_filename', nargs='+', type=str)
        parser.add_argument('forms_filename', nargs='+', type=str)
        parser.add_argument('formdata_filename', nargs='+', type=str)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        overviews_filename = kwargs['overviews_filename']
        forms_filename = kwargs['forms_filename']
        formdata_filename = kwargs['formdata_filename']

        try:
            answers = FormAnswer.objects.all()
            yes = answers.filter(text__iexact='yes').first()
            no = answers.filter(text__iexact='no').first()
            not_reviewed = answers.filter(text__iexact='not reviewed').first()
            does_not_exist = answers.filter(text__iexact='does not exist').first()
            partially = answers.filter(text__iexact='partially exists').first()
            need_improv = answers.filter(text__iexact='needs improvement').first()
            exist = answers.filter(text__iexact='exists, could be strengthened').first()
            high_performance = answers.filter(text__iexact='high performance').first()

            # Old mapping of the answers
            # key = CSV value, value = current value
            answerDict = {
                0: no.id,
                1: yes.id,
                2: not_reviewed.id,
                3: does_not_exist.id,
                4: partially.id,
                5: need_improv.id,
                6: exist.id,
                7: high_performance.id
            }

            overviews = []
            with open(overviews_filename, 'r') as ov:
                ov_reader = csv.reader(ov, delimiter=',')
                ov_fieldnames = next(ov_reader)
                ov_rows = list(ov_reader)

                for ovrow in ov_rows:
                    date_of_assessment = ovrow[0]
                    type_of_assessment = AssessmentType.objects.filter(name__iexact=ovrow[1])\
                                                               .values_list('id', flat=True)\
                                                               .first()
                    branches_involved = ovrow[2]
                    ns_focal_point_name = ovrow[3]
                    ns_focal_point_email = ovrow[4]
                    facilitator_name = ovrow[5]
                    facilitator_email = ovrow[6]
                    facilitator_contact = f'Skype: {ovrow[7]}'
                    date_of_mid_term_review = ovrow[8]
                    date_of_next_asmt = ovrow[9]
                    country_id = ovrow[10]
                    user_id = ovrow[11]

                    overview = Overview.objects.create(
                        date_of_assessment=date_of_assessment,
                        type_of_assessment=type_of_assessment,
                        branches_involved=branches_involved,
                        ns_focal_point_name=ns_focal_point_name,
                        ns_focal_point_email=ns_focal_point_email,
                        facilitator_name=facilitator_name,
                        facilitator_email=facilitator_email,
                        facilitator_contact=facilitator_contact,
                        date_of_mid_term_review=date_of_mid_term_review,
                        date_of_next_asmt=date_of_next_asmt,
                        country_id=country_id,
                        user_id=user_id
                    )
                    overviews.append(overview)

                    # For each Area create a Form record (Overview is the parent)
                    areas = FormArea.objects.values_list('id', flat=True)
                    form_data_to_create = []
                    for aid in areas:
                        form = Form.objects.create(
                            area_id=aid,
                            user_id=user_id,
                            overview_id=overview.id
                        )

                        # For each Question create a FormData record (Form is the parent)
                        questions = FormQuestion.objects.filter(component__area_id=aid).values_list('id', flat=True)
                        for qid in questions:
                            form_data_to_create.append(
                                FormData(
                                    form=form,
                                    question_id=qid
                                )
                            )
                    FormData.objects.bulk_create(form_data_to_create)

            # Run through the Form and FormData rows and try to match them to Overviews
            with open(forms_filename, 'r') as f, open(formdata_filename, 'r') as fd:
                f_reader = csv.reader(f, delimiter=',')
                f_fieldnames = next(f_reader)
                f_rows = list(f_reader)

                fd_reader = csv.reader(fd, delimiter=',')
                fd_fieldnames = next(fd_reader)
                fd_rows = list(fd_reader)

                for frow in f_rows:
                    # Check if we just created an Overview for the relevant country
                    # (there were Forms without an Overview...)
                    overview = None
                    for ov in overviews:
                        if not overview and ov.country_id == frow[3]:
                            overview = ov

                    forms = []
                    if not overview:
                        overview = Overview.objects.create(
                            date_of_assessment=timezone.now(),
                            type_of_assessment=AssessmentType.objects.filter(name__iexact='self assessment'),
                            country_id=frow[3],
                            user_id=frow[2]
                        )

                        # Bit of a code duplication, but we won't use this much more
                        # than the initial import
                        # For each Area create a Form record (Overview is the parent)
                        areas = FormArea.objects.values_list('id', flat=True)
                        form_data_to_create = []
                        for aid in areas:
                            form = Form.objects.create(
                                area_id=aid,
                                user_id=user_id,
                                overview_id=overview.id
                            )
                            forms.append(form)

                            # For each Question create a FormData record (Form is the parent)
                            questions = FormQuestion.objects.filter(component__area_id=aid).values_list('id', flat=True)
                            for qid in questions:
                                form_data_to_create.append(
                                    FormData(
                                        form=form,
                                        question_id=qid
                                    )
                                )
                        FormData.objects.bulk_create(form_data_to_create)
                    else:
                        forms = list(Form.objects.filter(overview_id=overview.id))

                    form = Form.objects.filter(overview_id=overview.id, area__area_num=frow[1]).first()

                    for formdata in fd_rows:
                        # TODO: match formdata with forms
                        return

                    # form_data_in_db = FormData.objects.filter(form_id=form.id)
                    # questions = FormQuestion.objects.filter(component__area_id=aid).values_list('id', flat=True)
                    # for qid in questions:
                    #     form_data = form_data_in_db.filter(question_id=qid).first()
                        
                    #     else:
                    #         if form_data.selected_answer_id != questions[qid]['selected_answer'] \
                    #                 or form_data.notes != questions[qid]['notes']:
                    #             form_data.selected_answer_id = questions[qid]['selected_answer'] or form_data.selected_answer_id
                    #             form_data.notes = questions[qid]['notes'] or form_data.notes
                    #             form_data.save()
            print('done!')
        except Exception as e:
            print('FAILED')
            print(e)
