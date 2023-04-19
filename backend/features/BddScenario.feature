@test
Feature:Low code App
Scenario Outline:Orthogonal Testing Validation for Demo Website- Appointment Page
Given I launch Demo Health Tracking Application URL 
When I login to the application with the defined credentials 
And I select the Appointments Tab 
And I select the Add Appointment option 

And Funrnish the information "<type>","<method>","<patient>","<provider>"

And I add the other details to the form 
And I select cancel the appointment device 
And I logout from the application 
And I verify the logout message 


Examples:
|type|method|patient|provider|
|Emergency|Call|John Doe|Henry Taylor|
|Emergency|Call|John Doe|Henry Taylor|
|Emergency|Referral|John Doe|Henry Taylor|
|Emergency|Referral|John Doe|Henry Taylor|
|Telephone|Call|John Doe|Henry Taylor|
|Telephone|Call|John Doe|Henry Taylor|
|Telephone|Referral|John Doe|Henry Taylor|
|Telephone|Referral|John Doe|Henry Taylor|
