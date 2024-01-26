from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_result_with_selenium_and_save(registration_number):
    url = "http://lms.uaf.edu.pk/login/index.php"  # Replace with your actual URL

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver with headless options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the form page
        driver.get(url)

        # Find the registration input field and submit button
        reg_input = driver.find_element(By.NAME, "Register")
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Result']")

        # Enter the registration number
        reg_input.send_keys(registration_number)

        # Click the submit button
        submit_button.click()

        # Wait for the result page to load (you may need to adjust the wait time)
        driver.implicitly_wait(10)

        # Get the result page content
        result_content = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(result_content, 'html.parser')

        # Extract Registration and Name from the first table
        registration = soup.find('table', class_='table tab-content').find('td', text='Registration #').find_next('td').text.strip()
        name = soup.find('table', class_='table tab-content').find('td', text='Student Full Name').find_next('td').text.strip()

        # Create custom HTML for the head section
        head_html = f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>UAF CGPA Calculator</title>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <main class="table" id="customers_table">
                <section class="table__header">
                    <h1><span style="color: rgb(205, 35, 171);">Registration#</span> <span style="color: rgb(15, 72, 158);">{registration}</span></h1>
                    <h1><span style="color: rgb(205, 35, 171);">Name:</span> <span style="color: rgb(15, 72, 158);">{name}</span></h1>

                    <div>
                        <button type="button" class="button">Download PDF</button>
                    </div>
                </section>
        """

        # Extract and create custom HTML for the second table
        result_table = soup.find_all('table', class_='table tab-content')[1]
        result_table_html = str(result_table)

        # Find the index of the "Semester" column
        headers = result_table.find_all('th')
        semester_index = headers.index(result_table.find('th', text='Semester'))

        # Group rows based on the values in the "Semester" column
        semester_rows = {}
        sr_counter = 1  # Reset Sr counter for each semester
        for row in result_table.find_all('tr')[1:]:
            semester_value = row.find_all('td')[semester_index].get_text(strip=True)
            if semester_value not in semester_rows:
                semester_rows[semester_value] = []
                sr_counter = 1  # Reset Sr counter for each semester
            # Update the Sr column with the reset counter
            row.find('td', text=str(row.find('td', text=True).get_text(strip=True))).string = str(sr_counter)
            sr_counter += 1
            semester_rows[semester_value].append(str(row))

        # Combine all semester tables into a single HTML string
        all_semesters_html = ""
        for semester, rows in semester_rows.items():
            # Add a heading for each semester
            semester_heading = f"<div class='parent-container'><h2 class='hd'>{semester}</h2></div>"
            semester_html = f"{semester_heading}<section class=\"table__body\"><table class=\"table tab-content\"><tr>{result_table_html.split('<tr>')[1]}{''.join(rows)}</tr></table></section>"
            all_semesters_html += semester_html

        # Save the combined result to a single HTML file
        filename = f"{registration_number}_all_semesters.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(head_html + all_semesters_html + "</main></body></html>")
        print(f"All semesters result saved to {filename}")

        # Wait for a few seconds before closing the browser
        time.sleep(5)

    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":
    registration_number = input("Enter your Registration Number (****-ag-****): ")
    get_result_with_selenium_and_save(registration_number)
