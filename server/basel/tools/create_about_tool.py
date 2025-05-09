import logging
from llama_index.core.tools.function_tool import FunctionTool

logger = logging.getLogger(__name__)


def get_about() -> str:
    about = """
    Basel is your AI Career Companion designed to empower users in their job search and career growth. Users
    build and maintain their resumes, take and prepare for interviews, and connect with potential employers more effectively.

    Key Features:
    - Personalized Career Assistance: Users can log in, enabling Basel to generate conversation summaries and keep track of details 
    that enhance career planning.
    - Shareable Links: Users can create and share secure links, allowing potential employers and recruiters to chat with their Basel
    in order to learn about their skills, strengths, and qualifications. Visitors accessing these links do not need to sign in. Users are to share
    these links in applications, resumes, and directly with recruiters/employers.
    - Interviews: Users can participate in interviews, which are created by administrators. Interviews are generated by Basel based on actual job postings.
    You are able to take the simulated interview and have your responses recorded. Additionally, Basel provides application links so that you can embed
    a `Shareable Link` into the application so that the recruiter/employer can see how you responded to the auto-generated interview for the specific position.
    - Standups: Basel enourages you to interact on a daily basis so that she can learn more about you over time with `standups`. Each day,
    log previous progress (yesterday), next steps (today), and any blockers you might be experiencing. Basel records progress and becomes more interactive
    over time.
    - Dynamic Resume: Maintaining Your Career Story Over Time. Basel serves as more than just a static resume – it’s a dynamic career 
    hub. Unlike traditional resumes that require constant manual updates, Basel continuously enhances your profile as you engage 
    with the platform. Through automated interviews and regular conversations, Basel captures new experiences, skills, 
    and achievements, transforming your resume into a living document that evolves with your career. Simply ask her to make a resume for you 
    at any time.
    - Translation and Technical Barriers: Often when chatting with recruiters there is a language or technical barrier that is hard to translate.
    When recruiters talk with your bot, they are able to receive the information in a way that highlights your strengths through language that makes 
    sense to them.
    """
    return about


def create_about_tool():
    get_interviews_tool = FunctionTool.from_defaults(
        fn=get_about,
        name="get_about_basel_tool",
        description="""
        Useful if the user asks about what Basel or the Platform is or needs help with what the platform does.
        Provides an indepth system/platform description. This can include:
        - Interviews
        - Shareable Links
        - Dynamic Resumes
        - Standups
        """,
    )

    return get_interviews_tool
