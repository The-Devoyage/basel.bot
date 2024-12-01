import logging
from llama_index.core.tools.function_tool import FunctionTool

logger = logging.getLogger(__name__)


def get_about() -> str:
    about = """
    Basel is a Career Assistant platform designed to empower users in their job search and career growth. With the help of an AI bot named Basel, users can build and maintain their resumes, prepare for interviews, and connect with potential employers more effectively.

    Key Features:
    Personalized Career Assistance: Users can log in, enabling Basel to generate conversation summaries and keep track of details that enhance career planning.
    Secure Sharing: Users can create and share secure links, allowing others to chat with Basel to learn about their skills, strengths, and qualifications. Visitors accessing these links do not need to sign in.
    Interview Preparation: Users can participate in interviews, which are currently created and managed by Admins.
    By combining open-ended conversations with Basel and guided interview sessions, the platform gathers valuable insights to present users in the best possible light to recruiters and potential employers.

    Automated Interviews: Keeping Your Profile Up-to-Date
    Basel's automated interviews provide a seamless way to keep your professional profile current. Through regular interview sessions, Basel gathers information about your recent accomplishments, new skills, and evolving career goals. This ensures that your profile remains relevant and aligned with industry trends. Whether you've taken up a new certification, completed a successful project, or shifted career focus, Basel captures these updates and integrates them into your dynamic resume automatically. This eliminates the need for manual updates and ensures your profile is always ready for the next opportunity.

    Career Assistant Bot: Matching Candidates to Employers
    Basel's AI bot acts as a bridge between candidates and employers. Using the information gathered through conversations and interviews, Basel identifies key strengths, experiences, and qualifications that align with employer needs. The bot's ability to analyze job descriptions and compare them to a user’s profile makes it an invaluable tool for tailored job recommendations. Whether you're seeking a role in technology, healthcare, or any other industry, Basel uses its deep insights to connect you with roles that match your skills and career aspirations.

    Job Search: Sharing Secure Links
    Basel simplifies the job search process by enabling users to create secure, shareable links. These links allow recruiters, potential employers, or professional connections to chat with Basel directly and learn about your qualifications without needing to log in.

    Example Sharing Methods:
    Email: Include the secure link in your job application emails or responses to recruiters.
    Social Media: Share your link on LinkedIn, Twitter, or professional forums to expand your reach.
    This innovative feature ensures your profile is always accessible, while maintaining control and security over your information.

    Dynamic Resume: Maintaining Your Career Story Over Time
    Basel serves as more than just a static resume – it’s a dynamic career hub. Unlike traditional resumes that require constant manual updates, Basel continuously enhances your profile as you engage with the platform. Through automated interviews and regular conversations, Basel captures new experiences, skills, and achievements, transforming your resume into a living document that evolves with your career.

    With Basel:

    Real-Time Updates: Your resume grows alongside your career journey, always reflecting the latest version of your professional self.
    Customizable Presentations: Tailor your dynamic resume for different roles by highlighting relevant skills and experiences.
    Secure and Portable: Easily share your resume via secure links or download a tailored version for specific applications.
    By maintaining a dynamic resume, you stay prepared for opportunities as they arise, ensuring recruiters see the most accurate and compelling representation of your career.

    Basel isn’t just a career assistant—it’s your partner in achieving career success, helping you stay ahead in today’s competitive job market.
    """
    return about


def create_about_tool():
    get_interviews_tool = FunctionTool.from_defaults(
        fn=get_about,
        name="get_about_basel_tool",
        description="""
        Useful if the user asks about what Basel or the Platform is.
        Provides an indepth system/platform description.
        """,
    )

    return get_interviews_tool
