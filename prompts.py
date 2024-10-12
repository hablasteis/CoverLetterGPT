cover_letter_system_prompt = "You are an assistant tasked with writing the most persuasing and effective cover letters."

simplify_style_prompt = "Write like a 25yo graduate not english native would write, not like a 50yo native person"

cover_letter_prompt = f"""
# JOB AD #

{{job_title}}

{{job_ad}}

# CONTEXT (My CV) #

{{cv}}

# OBJECTIVE #
{{objective}}

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