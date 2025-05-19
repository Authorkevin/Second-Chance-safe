from django.shortcuts import render, redirect

def home(request):
	return render(request, "home.html")

def voter_registration(request):
	return render(request, "voter_registration.html")

def quizzes(request):
	return render(request, "quizzes.html")

def quiz_platform(request):
	return render(request, "quiz_platform.html")

def quiz_voter(request):
	if request.method == "POST":
		acount = 0
		bcount = 0
		ccount = 0
		dcount = 0

        # request.POST is a dictionary-like object containing submitted form data
        # We need to iterate through the specific question fields (e.g., 'q1', 'q2', etc.)
		for key, value in request.POST.items():
			if key.startswith('q'):  # Only process fields that start with 'q' (our questions)
                		if value == 'a':
                	    		acount += 1
                		elif value == 'b':
                	    		bcount += 1
                		elif value == 'c':
                	    		ccount += 1
                		elif value == 'd':
                	    		dcount += 1

		
		if acount > bcount and acount > ccount and acount > dcount:
			result = 'Your views align most closely with: policies that focus on community-driven development, emphasizing government investment in infrastructure, education, and tribal sovereignty, especially in underdeveloped areas. You may prefer Democratic platforms that emphasize social programs, expanded healthcare, and government support for Native American and rural communities.'
		elif bcount > acount and bcount > ccount and bcount > dcount:
			result = 'Your views align most closely with: market-driven solutions with a focus on business incentives, tax cuts, and less government intervention in individual matters. You may align with Republican platforms that emphasize deregulation, lower taxes, and encouraging private-sector growth in underserved areas.'
		elif ccount > acount and ccount > bcount and ccount > dcount:
			result = 'Your views align most closely with: policies that focus on sustainability, environmentally friendly development, and self-sufficiency in rural and Native American communities. You may find common ground with progressive or centrist policies that support green initiatives and long-term economic independence.'
		elif dcount > acount and dcount > bcount and dcount > ccount:
 			result = 'Your views align most closely with: policies that align with autonomy and independent decision-making for communities. You may support policies that give local governments and individual communities more control over their economic and social affairs, with a focus on less reliance on the state or federal government.'
		else:
			result = "It's difficult to determine a strong alignment based on your responses." # Handle ties or no clear majority

        # Render the template and pass the 'result' variable to it
		result_title = "YOUR RESULTS"
		return render(request, 'quiz_voter_rights.html', {'result_title': result_title, 'result': result})
	else:
        # If the request method is not POST (e.g., the user just opened the quiz page)
        # render the empty quiz form
        	return render(request, "quiz_voter_rights.html")

def quiz_candidate(request):
	if request.method == "POST":
                acount = 0
                bcount = 0
                ccount = 0
                dcount = 0

        # request.POST is a dictionary-like object containing submitted form data
        # We need to iterate through the specific question fields (e.g., 'q1', 'q2', etc.)
                for key, value in request.POST.items():
                        if key.startswith('q'):  # Only process fields that start with 'q' (our questions)
                                if value == 'a':
                                        acount += 1
                                elif value == 'b':
                                        bcount += 1
                                elif value == 'c':
                                        ccount += 1
                                elif value == 'd':
                                        dcount += 1


                if acount > bcount and acount > ccount and acount > dcount:
                        result = "You chose A the most. After taking the quiz, evaluate the qualities that you elected most frequently. These are the qualities and actions that are most important to you in a local leader. Look for candidates who: Focus on the issues that matter most to you (water, healthcare, education, jobs, etc.). Have a leadership style that aligns with your preferences (collaborative, action-oriented, or community-based). Demonstrate transparency, honesty, and integrity. Have a proven track record in solving similar problems in the community. Seek to involve you and your neighbors in important decisions. By considering these traits, you can choose a candidate who is committed to addressing your community’s needs and improving life for everyone. Don’t know where to start? Presidential Election Quiz- https://www.opencampaign.com/quiz – this website also lets you search your area for who represents you, where they stand on issues, voting record and where they get their support from. Guides.vote- https://guides.vote/ – Provides clear, insightful, and well-sourced nonpartisan information oncandidate positions to help voters stay informed and understand their stance on important issues."
                elif bcount > acount and bcount > ccount and bcount > dcount:
                        result = "You chose B the most. After taking the quiz, evaluate the qualities that you elected most frequently. These are the qualities and actions that are most important to you in a local leader. Look for candidates who: Focus on the issues that matter most to you (water, healthcare, education, jobs, etc.). Have a leadership style that aligns with your preferences (collaborative, action-oriented, or community-based). Demonstrate transparency, honesty, and integrity. Have a proven track record in solving similar problems in the community. Seek to involve you and your neighbors in important decisions. By considering these traits, you can choose a candidate who is committed to addressing your community’s needs and improving life for everyone. Don’t know where to start? Presidential Election Quiz- https://www.opencampaign.com/quiz – this website also lets you search your area for who represents you, where they stand on issues, voting record and where they get their support from. Guides.vote- https://guides.vote/ – Provides clear, insightful, and well-sourced nonpartisan information oncandidate positions to help voters stay informed and understand their stance on important issues."
                elif ccount > acount and ccount > bcount and ccount > dcount:
                        result = "You chose C the most. After taking the quiz, evaluate the qualities that you elected most frequently. These are the qualities and actions that are most important to you in a local leader. Look for candidates who: Focus on the issues that matter most to you (water, healthcare, education, jobs, etc.). Have a leadership style that aligns with your preferences (collaborative, action-oriented, or community-based). Demonstrate transparency, honesty, and integrity. Have a proven track record in solving similar problems in the community. Seek to involve you and your neighbors in important decisions. By considering these traits, you can choose a candidate who is committed to addressing your community’s needs and improving life for everyone. Don’t know where to start? Presidential Election Quiz- https://www.opencampaign.com/quiz – this website also lets you search your area for who represents you, where they stand on issues, voting record and where they get their support from. Guides.vote- https://guides.vote/ – Provides clear, insightful, and well-sourced nonpartisan information oncandidate positions to help voters stay informed and understand their stance on important issues."
                elif dcount > acount and dcount > bcount and dcount > ccount:
                        result = "You chose D the most. After taking the quiz, evaluate the qualities that you  elected most frequently. These are the qualities and actions that are most important to you in a local leader. Look for candidates who: Focus on the issues that matter most to you (water, healthcare, education, jobs, etc.). Have a leadership style that aligns with your preferences (collaborative, action-oriented, or community-based). Demonstrate transparency, honesty, and integrity. Have a proven track record in solving similar problems in the community. Seek to involve you and your neighbors in important decisions. By considering these traits, you can choose a candidate who is committed to addressing your community’s needs and improving life for everyone. Don’t know where to start? Presidential Election Quiz- https://www.opencampaign.com/quiz – this website also lets you search your area for who represents you, where they stand on issues, voting record and where they get their support from. Guides.vote- https://guides.vote/ – Provides clear, insightful, and well-sourced nonpartisan information oncandidate positions to help voters stay informed and understand their stance on important issues."
                else:
                        result = "It's difficult to determine a strong alignment based on your responses. After taking the quiz, evaluate the qualities that you elected most frequently. These are the qualities and actions that are most important to you in a local leader. Look for candidates who: Focus on the issues that matter most to you (water, healthcare, education, jobs, etc.). Have a leadership style that aligns with your preferences (collaborative, action-oriented, or community-based). Demonstrate transparency, honesty, and integrity. Have a proven track record in solving similar problems in the community. Seek to involve you and your neighbors in important decisions. By considering these traits, you can choose a candidate who is committed to addressing your community’s needs and improving life for everyone. Don’t know where to start? Presidential Election Quiz- https://www.opencampaign.com/quiz – this website also lets you search your area for who represents you, where they stand on issues, voting record and where they get their support from. Guides.vote- https://guides.vote/ – Provides clear, insightful, and well-sourced nonpartisan information oncandidate positions to help voters stay informed and understand their stance on important issues." # Handle ties or no clear majority

        # Render the template and pass the 'result' variable to it
                result_title = "YOUR RESULTS"
                return render(request, 'quiz_candidate.html', {'result_title': result_title, 'result': result})
	else:
		return render(request, "quiz_candidate.html")

def about(request):
	return render(request, "about.html")
