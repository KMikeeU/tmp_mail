import temp_mail


# ---- Example Script -----
# This example script will set up a random email address,
# wait for new emails and print every link contained in
# them. Please use this respectfully.



# Setup a new email address by random, supply an email as
# an argument to force it's use
mail = temp_mail.Client()

# printing the randomly generated email address
print(mail.address)


# Defining a callback to use later
def cb(m):
	# Print all the links which are contained in the email
	print(m.links())


# Listen for new emails, whenever a new email is received
# cb is called with an Email object as the argument

mail.checkloop(async=False, callback=cb)