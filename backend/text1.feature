@Dev
Scenario Outline:Seat Booking
Given I launch SeatBooking Application URL
When I Login to SeatBooking Application
And I land to SeatBooking Application Home Page
And I Click on button Make Reservation
And Funrnish the information "<a>","<b>","<c>","<d>"
And Clicks on button Make Reservation button and verify the message
And I logout from WebGantt application
Examples:
|a|b|c|d|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
|0|0|0|0|
