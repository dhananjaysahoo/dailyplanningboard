from django.db import models

# Create your models here.

status_option = (
                ('Open','Open'),
                ('Inprogress','Inprogress'),
                ('Completed','Completed')
                )
priority_option = (
                  ('High', 'High'),
                  ('Medium', 'Medium'),
                  ('Low', 'Low')
                  )
unitSys_option = (
                  ('CFBC','CFBC'),
                  ('AHS','AHS'),
                  ('MHS','MHS'),
                  ('LIME','LIME'),
                  ('UB','UB'),
                  ('HRSG','HRSG'),
                  ('GT','GT'),
                  ('STG','STG'),
                  ('CPP-BOP','CPP-BOP'),
                  ('CFBC-BOP','CFBC-BOP'),
                  ('IA/PA/IG','IA/PA/IG'),
                  ('SW/PW','SW/PW'),
                  ('Switch-Yard','Switch-Yard'),
                  ('SS-9','SS-9'),
                  ('SS-10','SS-10'),
                  ('SS-29','SS-29'),
                  ('SS-30','SS-30'),
                  ('MRS-80','MRS-80'),
                  ('VAM/Chiller','VAM/Chiller'),
                  ('AHU/APU','AHU/APU'),
                  ('Fire','Fire'),
                  ('OWS','OWS'),
                  ('OT-DRAIN','OT-DRAIN'),
                  ('TRAFO','TRAFO'),
                  ('RFG','RFG'),
                  ('NG','NG'),
                  ('LCO','LCO'),
                  ('NAPHTHA','NAPHTHA'),
                  ('HSD','HSD'),
                  ('Flare','Flare'),
                  ('Pet-Coke','Pet-Coke'),
                  )
department_option = (
                  ('MMD', 'MMD'),
                  ('EMD', 'EMD'),
                  ('IMD', 'IMD')
                  )
permit_option = (
                  ('Cold', 'Cold'),
                  ('Hot', 'Hot'),
                  ('Confined','Confined'),
                  )
remarks_option = (
                  ('CM', 'CM'),
                  ('PM', 'PM'),
                  ('NMS', 'NMS'),
                  ('MI', 'MI'),
                  ('SD', 'SD'),
                  ('GT-MI', 'GT-MI'),
                  ('Defect', 'Defect'),
                  ('HouseKeeping', 'HouseKeeping'),
                  ('Lubrication', 'Lubrication'),
                  )


class TaskList(models.Model):
    UnitSystem = models.CharField(max_length=20, choices=unitSys_option, blank=True)
    Department = models.CharField(max_length=20, choices=department_option, blank=True)
    Permit = models.CharField(max_length=20, choices=permit_option, blank=True)
    SAPNum = models.CharField(max_length=60, blank=True)
    Description = models.CharField(max_length=500, blank=True)
    Remarks = models.CharField(max_length=20, choices=remarks_option, blank=True)
    Priority = models.CharField(max_length=20, choices=priority_option, blank=True)
    Status = models.CharField(max_length=20, choices=status_option, blank=True)
    CreatedDate = models.CharField(max_length=20, blank=True)
    LastActivity = models.CharField(max_length=20, blank=True)
    MonthYearID = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f" {self.id}: {self.UnitSystem} {self.Department} {self.Permit} {self.SAPNum} {self.Description} {self.Remarks} {self.Priority} {self.Status} {self.CreatedDate} {self.LastActivity} {self.MonthYearID}"


