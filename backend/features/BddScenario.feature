@test
Feature:Low code App
Scenario Outline:Orthogonal Testing Validation for Demo Website
Given I launch Demo Health Tracking Application URL 
When I login to the application with the defined credentials 
And I select the Appointments Tab 
And I select the Add Appointment option 

And Funrnish the information "<type>","<method>","<patient>","<provider>"

And I add the other details to the form 
And I save the appointment device 
And I procceed to delete the appointment 
And I logout from the application 
And I verify the logout message 


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
