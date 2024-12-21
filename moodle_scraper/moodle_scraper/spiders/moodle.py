import scrapy
from scrapy.http import FormRequest

class MoodleSpider(scrapy.Spider):
    name = "moodle"
    allowed_domains = ["sandbox.moodledemo.net"]
    start_urls = ["https://sandbox.moodledemo.net/login/index.php"]

    # Replace with your actual credentials
    username = 'student'  # Your Moodle username
    password = 'sandbox24'   # Your Moodle password

    def parse(self, response):
        # Find the login form and fill in the fields
        return FormRequest.from_response(
            response,
            formxpath='//form[@id="login"]',  # Adjust the form xpath if necessary
            formdata={
                'username': self.username,
                'password': self.password
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # Check if login succeeded
        if "Invalid login" in response.text:
            self.log("Login failed!")
            return

        self.log("Login succeeded!")

        # Scrape course titles - Adjust the selectors according to the actual HTML structure
        courses = response.css('.coursebox')

        for course in courses:
            title = course.css('.coursename a::text').get()
            link = course.css('.coursename a::attr(href)').get()
            teacher = course.css('.teachers a::text').get()

            yield {
                'course_title': title,
                'course_link': link,
                'teacher_name': teacher,
            }
    

