from google import genai
from config import get_settings

settings = get_settings()


class AIService:
    def __init__(self):
        # Use the new Google GenAI API with gemini-2.5-flash
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = "gemini-2.5-flash"
    
    async def generate_section_content(self, topic: str, section_title: str, document_type: str) -> str:
        """Generate content for a specific section/slide based on the topic and section title."""
        
        if document_type == "pptx":
            prompt = f"""
You are creating content for a PowerPoint presentation about: {topic}

Generate content for this slide: {section_title}

Requirements:
- Write 3-5 concise bullet points
- Each bullet should be clear and impactful
- Use professional language
- Focus on key insights relevant to the slide title
- Keep each bullet to 1-2 lines

Return only the bullet points, one per line, starting with a dash (-).
"""
        else:  # docx
            prompt = f"""
You are writing a professional document about: {topic}

Generate content for this section: {section_title}

Requirements:
- Write 2-3 well-structured paragraphs
- Use professional and clear language
- Provide informative and relevant content
- Each paragraph should be 3-5 sentences
- Focus on the section topic

Return only the paragraph text, separated by blank lines.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    async def refine_content(self, current_content: str, refinement_prompt: str, section_title: str) -> str:
        """Refine existing content based on user's refinement request."""
        
        prompt = f"""
You are refining content for a section titled: {section_title}

Current content:
{current_content}

User's refinement request: {refinement_prompt}

Please revise the content according to the user's request while maintaining professionalism and clarity.
Return only the refined content.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Error refining content: {str(e)}"
    
    async def generate_outline(self, topic: str, document_type: str, num_sections: int = 5) -> list:
        """Generate an outline/structure for the document."""
        
        if document_type == "pptx":
            prompt = f"""
Create a PowerPoint presentation outline about: {topic}

Generate exactly {num_sections} slide titles.

Requirements:
- First slide should be a title/introduction
- Last slide should be a conclusion or call-to-action
- Middle slides should cover key aspects of the topic
- Each title should be concise (3-7 words)
- Use professional language

Return only the slide titles, one per line, numbered.
"""
        else:  # docx
            prompt = f"""
Create a document outline about: {topic}

Generate exactly {num_sections} section headings.

Requirements:
- First section should be an introduction
- Last section should be a conclusion
- Middle sections should cover key aspects of the topic
- Each heading should be clear and descriptive
- Use professional language

Return only the section headings, one per line, numbered.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            lines = response.text.strip().split('\n')
            # Clean up the titles (remove numbering, extra whitespace)
            titles = []
            for line in lines:
                line = line.strip()
                if line:
                    # Remove common numbering patterns
                    import re
                    cleaned = re.sub(r'^\d+[\.\)]\s*', '', line)
                    cleaned = re.sub(r'^[-•*]\s*', '', cleaned)
                    if cleaned:
                        titles.append(cleaned)
            
            return titles[:num_sections]
        except Exception as e:
            # Fallback to generic titles
            if document_type == "pptx":
                return [f"Slide {i+1}" for i in range(num_sections)]
            else:
                return [f"Section {i+1}" for i in range(num_sections)]


ai_service = AIService()
