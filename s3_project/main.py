# Imports the class to create the structure for the database. Can run the class by specifying 'to_create' = True upon
# instantiation, or by running the .run_methods()

from s3_project.classes.create_database import ProjectDatabase
new = ProjectDatabase(to_create=False)


# # To move to top of joining tables:
# from s3_project.classes.applicant_info_class import ApplicantInfoClean
# from s3_project.classes.academy_class import Academy
# from s3_project.classes.talent_csv_cleaning import TalentCsv
# from s3_project.classes.cleaning_txt import TextFiles
#
#
# talent_applicant_info = ApplicantInfoClean()
# academy_dataframe = Academy()
# monthly_talent_info = TalentCsv()
# talent_txt = TextFiles()
