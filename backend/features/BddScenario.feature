@
Feature:Low code App
Scenario Outline:
 

And Funrnish the information "<type>","<method>","<patient>","<provider>"

 


Examples:
|type|method|patient|provider|
|Appointment 1|Call|Patient1|Provider Name 1|
|Appointment 1|Call|Patient2|Provider Name 2|
|Appointment 1|Referral|Patient1|Provider Name 2|
|Appointment 1|Referral|Patient2|Provider Name 1|
|Appointment 2|Call|Patient1|Provider Name 2|
|Appointment 2|Call|Patient2|Provider Name 1|
|Appointment 2|Referral|Patient1|Provider Name 1|
|Appointment 2|Referral|Patient2|Provider Name 2|
