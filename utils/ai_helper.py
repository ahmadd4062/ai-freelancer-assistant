from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
import os
from xhtml2pdf import pisa
from google import genai
import re

# Initialize the client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Use the working model from your test
WORKING_MODEL = "gemini-3.1-flash-lite"

def generate_proposal(proposal_data):
    """
    Generate a professional proposal using Google Gemini API
    """
    prompt = f"""
    Create a professional proposal for a freelance project with the following details:
    
    Client Name: {proposal_data.client_name}
    Project Title: {proposal_data.project_title}
    Project Description: {proposal_data.project_description}
    Skills: {', '.join(proposal_data.get_skills_list())}
    Budget: ${proposal_data.budget}
    Timeline: {proposal_data.timeline}
    Tone: {proposal_data.get_tone_display()}
    
    Please write a complete proposal that includes:
    1. A professional introduction
    2. Understanding of the project
    3. How my skills match the project requirements
    4. Proposed approach and methodology
    5. Timeline breakdown
    6. Budget breakdown
    7. Professional closing
    
    Make it persuasive and tailored to the client's needs.
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating proposal: {str(e)}"

def generate_cover_letter(coverletter_data):
    """
    Generate a professional cover letter using Google Gemini API
    """
    prompt = f"""
    Create a professional cover letter for a job application with the following details:
    
    Job Title: {coverletter_data.job_title}
    Company Name: {coverletter_data.company_name}
    Experience: {coverletter_data.experience}
    Skills: {', '.join(coverletter_data.get_skills_list())}
    Portfolio URL: {coverletter_data.portfolio_url or 'Not provided'}
    Tone: {coverletter_data.get_tone_display()}
    
    Please write a complete cover letter that includes:
    1. Professional greeting
    2. Introduction expressing interest in the position
    3. Highlight relevant experience
    4. Match skills to job requirements
    5. Professional closing
    
    Make it compelling and tailored to the company.
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

def render_to_pdf(template_src, context_dict={}):
    """Convert HTML template to PDF"""
    template = get_template(template_src)
    html = template.render(context_dict)
    
    # Create response
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="proposal.pdf"'
    
    # Create PDF with better error handling
    pisa_status = pisa.CreatePDF(
        html,
        dest=result,
        link_callback=link_callback,
        encoding='utf-8'
    )
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

def link_callback(uri, rel):
    """Handle static files in PDF"""
    if uri.startswith('/static/'):
        path = os.path.join(settings.STATIC_ROOT, uri.replace('/static/', ''))
        return path
    return uri


def clean_ai_response(content):
    """Clean markdown formatting from AI response for PDF display"""
    if not content:
        return content
    
    # Remove markdown bold/italic
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'\*(.*?)\*', r'\1', content)
    
    # Replace markdown headings
    content = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', content)
    content = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', content)
    content = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', content)
    
    # Replace markdown lists
    content = re.sub(r'- (.*?)\n', r'• \1<br>', content)
    content = re.sub(r'\* (.*?)\n', r'• \1<br>', content)
    
    # Replace horizontal rules
    content = re.sub(r'---\n', r'<hr>\n', content)
    
    # Replace line breaks - preserve paragraphs
    content = re.sub(r'\n\n', r'<br><br>', content)
    content = re.sub(r'\n', r'<br>', content)
    
    return content


def generate_gig_description(gig_data):
    """
    Generate gig description, SEO keywords, and FAQ suggestions using Google Gemini API
    """
    prompt = f"""
    Create a complete gig description for a freelance service with the following details:
    
    Service Category: {gig_data.service_category}
    Skills: {', '.join(gig_data.get_skills_list())}
    Experience Level: {gig_data.get_experience_level_display()}
    Delivery Time: {gig_data.delivery_time}
    Features: {', '.join(gig_data.get_features_list())}
    Revisions: {gig_data.revisions}
    
    Please provide:
    
    1. A compelling gig description that includes:
       - An engaging introduction
       - What the service includes
       - Why the client should choose this service
       - What the client will receive
       
    2. SEO Keywords: List of 10 relevant keywords for this gig
    
    3. FAQ Suggestions: 5 frequently asked questions and answers
    
    Format your response as:
    DESCRIPTION: [gig description]
    SEO: [comma separated keywords]
    FAQ: [question1? Answer1. Question2? Answer2. ...]
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        
        content = response.text
        
        # Parse the response
        result = {}
        
        # Extract description
        import re
        desc_match = re.search(r'DESCRIPTION:\s*(.*?)(?=SEO:|$)', content, re.DOTALL)
        if desc_match:
            result['description'] = desc_match.group(1).strip()
        else:
            result['description'] = content
            
        # Extract SEO keywords
        seo_match = re.search(r'SEO:\s*(.*?)(?=FAQ:|$)', content, re.DOTALL)
        if seo_match:
            result['seo_keywords'] = seo_match.group(1).strip()
        else:
            result['seo_keywords'] = ''
            
        # Extract FAQ
        faq_match = re.search(r'FAQ:\s*(.*?)$', content, re.DOTALL)
        if faq_match:
            result['faq_suggestions'] = faq_match.group(1).strip()
        else:
            result['faq_suggestions'] = ''
        
        return result
    except Exception as e:
        return {
            'description': f"Error generating gig description: {str(e)}",
            'seo_keywords': '',
            'faq_suggestions': ''
        }
    

def generate_pricing_suggestions(pricing_data):
    """
    Generate pricing suggestions, market analysis, and service tips using Google Gemini API
    """
    prompt = f"""
    Analyze the following freelance project pricing and provide suggestions:
    
    Hourly Rate: ${pricing_data.hourly_rate}
    Estimated Hours: {pricing_data.estimated_hours}
    Complexity: {pricing_data.get_complexity_display()}
    Urgency: {pricing_data.get_urgency_display()}
    Additional Charges: ${pricing_data.additional_charges}
    Tax: ${pricing_data.tax}
    Calculated Price: ${pricing_data.calculate_suggested_price()}
    
    Please provide:
    
    1. Recommended Delivery Time: Suggest an optimal delivery time based on the project complexity and urgency.
    
    2. Market Analysis: Analyze if this pricing is competitive for the market. What's the typical range?
    
    3. Service Improvement Tips: Provide 3-5 tips to improve the service and justify higher rates.
    
    Format your response as:
    DELIVERY: [recommended delivery time]
    MARKET: [market analysis]
    TIPS: [tip1. tip2. tip3. ...]
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        
        content = response.text
        
        # Parse the response
        result = {}
        import re
        
        # Extract delivery
        delivery_match = re.search(r'DELIVERY:\s*(.*?)(?=MARKET:|$)', content, re.DOTALL)
        if delivery_match:
            result['recommended_delivery'] = delivery_match.group(1).strip()
        else:
            result['recommended_delivery'] = ''
            
        # Extract market analysis
        market_match = re.search(r'MARKET:\s*(.*?)(?=TIPS:|$)', content, re.DOTALL)
        if market_match:
            result['market_analysis'] = market_match.group(1).strip()
        else:
            result['market_analysis'] = ''
            
        # Extract tips
        tips_match = re.search(r'TIPS:\s*(.*?)$', content, re.DOTALL)
        if tips_match:
            result['service_tips'] = tips_match.group(1).strip()
        else:
            result['service_tips'] = ''
        
        return result
    except Exception as e:
        return {
            'recommended_delivery': f'Error: {str(e)}',
            'market_analysis': 'Unable to generate market analysis.',
            'service_tips': 'Please try again.'
        }
    
def generate_client_reply(reply_data):
    """
    Generate a professional client reply using Google Gemini API
    """
    prompt = f"""
    Generate a professional reply to a client message with the following details:
    
    Client Message: {reply_data.client_message}
    Tone: {reply_data.get_tone_display()}
    
    Please write a complete reply that:
    1. Acknowledges the client's message
    2. Addresses their concerns or questions
    3. Provides clear and helpful information
    4. Maintains a {reply_data.get_tone_display()} tone throughout
    5. Ends with a professional closing
    
    Make it clear, concise, and professional.
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating reply: {str(e)}"
    

def generate_contract(contract_data):
    """
    Generate a professional contract using Google Gemini API
    """
    prompt = f"""
    Generate a professional freelance contract with the following details:
    
    Client Name: {contract_data.client_name}
    Client Email: {contract_data.client_email}
    Client Company: {contract_data.client_company or 'N/A'}
    
    Freelancer Name: {contract_data.freelancer_name}
    Freelancer Email: {contract_data.freelancer_email}
    
    Project Title: {contract_data.project_title}
    Project Scope: {contract_data.project_scope}
    Timeline: {contract_data.timeline}
    
    Payment Terms: {contract_data.payment_terms}
    Total Amount: ${contract_data.total_amount}
    
    Terms & Conditions: {contract_data.terms_conditions}
    
    Start Date: {contract_data.start_date}
    End Date: {contract_data.end_date}
    
    Please write a complete professional contract that includes:
    1. Contract title and introduction
    2. Parties involved (Client and Freelancer)
    3. Project scope and deliverables
    4. Timeline and milestones
    5. Payment terms and schedule
    6. Terms and conditions
    7. Confidentiality clause
    8. Termination clause
    9. Governing law
    10. Signatures section
    
    Make it professional, legally sound, and well-structured.
    """
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating contract: {str(e)}"