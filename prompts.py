cover_letter_system_prompt = "You are an assistant tasked with writing the most persuasing and effective cover letters."

simplify_style_prompt = "Write like a 25yo graduate not english native would write, not like a 50yo native person"

cover_letter_prompt = f"""
# JOB AD #

{{job_title}}

{{job_ad}}

# CONTEXT (My CV) #

{{cv}}

# OBJECTIVE #
You are tasked with the following:
1. Make a list of all key elements from the JOB AD i.e. what the company wants in the candidate
2. Match these needs with my experiences and qualities in the CONTEXT. These can be vague matches too, but its critical to get as many quaities covered (however it's also critical to not lie in a way that they will find out)
3. Write a cover letter tailored to the matches 

# RESPONSE #
{simplify_style_prompt}
"""

dumb_down_prompt = f"""
# CONTEXT #
My cover letter:
{{cover_letter}}

# OBJECTIVE #
You are tasked with rewriting the letter in a more simple language style

# RESPONSE #
{simplify_style_prompt}
"""