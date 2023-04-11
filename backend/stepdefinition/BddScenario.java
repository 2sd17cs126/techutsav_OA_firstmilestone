public class seatbooking  {

	@Given("^I launch Demo Health Tracking Application URL$")
	public void I_launch_Demo_Health_Tracking_Application_URL() throws InterruptedException { Login.launchingURL()

	}

	@When("^I login to the application with the defined credentials$")
	public void I_login_to_the_application_with_the_defined_credentials() throws InterruptedException { driver=Login.login()

	}

	@And("^I select the Appointments Tab$")
	public void I_select_the_Appointments_Tab() throws InterruptedException { HomePage.appointment(driver)

	}

	@And("^I select the Add Appointment option$")
	public void I_select_the_Add_Appointment_option() throws InterruptedException { AppointmentPage.addnewappointment(driver)

	}

	@And("^I add the other details to the form$")
	public void I_add_the_other_details_to_the_form() throws InterruptedException { AppointmentPage.appointmentform(driver)

	}

	@And("^I save the appointment device$")
	public void I_save_the_appointment_device() throws InterruptedException { AppointmentPage.appointmentdetails(driver)

	}

	@And("^I procceed to delete the appointment$")
	public void I_procceed_to_delete_the_appointment() throws InterruptedException { AppointmentPage.saveappointment(driver)

	}

	@And("^I logout from the application$")
	public void I_logout_from_the_application() throws InterruptedException { AppointmentPage.deleteappointment(driver)

	}

	@And("^I verify the logout message$")
	public void I_verify_the_logout_message() throws InterruptedException { LogOut.accountoptions(driver)

	}

	
}