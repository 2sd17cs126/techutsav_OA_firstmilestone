Given('I launch Seat Booking Application {string}',(URL)=>{
ApplicationLaunch(URL)
})
When('I Login to Seat Booking Application {string},{string}',(Uname,Password)=>{
ApplicationLogin(Uname,Password)
})
And('I land to SeatBooking Application Home Page',()=>{

})
And('I Click on button Make Reservation',()=>{

})
And('Funrnish the information {string},{string},{string},{string}',(Model,Storage,Ram,Processor)=>{
userDefinedFunction(Model,Storage,Ram,Processor)
})
And('Clicks on button Make Reservation button and verify the message',()=>{

})
And('I logout from Web Gantt application',()=>{
ApplicationExit()
})
