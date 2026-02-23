Dear Sendify!

I met you at the Gösta career fair and was intrigued by what seemed like a great place to work and grow. Of course, I decided to apply to the summer internship but then I found this opportunity for fast-tracking the application, so here I am!

My Journey with this project:

Understanding MCP:
I had never heard of MCP prior to this, so I started by visiting their documentation. A skill I've developed during my studies is how to use LLMs to improve my learning (as opposed to impede - the trap which many students fall in), so I also asked lots of questions asking for pedagogical explanations. Whenever something didn't quite feel intuitive or right, it was of course important to fact check the robot.

Learning web scraping:
Automating website interaction is something I've had in mind for some projects that only ever stayed in my head, but with this I had no choice but to learn it. At first, I thought I would be parsing HTML using a simple request library but, of course, someone has always had the same problem as you have and there exists good libraries for most things. My approach to selecting a library to use was to describe the use case to an LLM and then ask it for suggestions with provided rationale. I got recommended Playwright, a library for automating web tests, and after looking into it for some time I decided to stick with it.

Choice of scraper tool:
Playwright launches an actual browser, that asynchronously waits for elements to load before trying to read the page.

How to test:
git clone https://github.com/VVikingsson/mcp-server.git
cd mcp-server/dbschenker_server
pip install uv OR powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv add mcp playwright

I used Claude Desktop, so the instructions are for it:
- Install Claude Desktop for your system
- Open the claude_desktop_config.json file
- Add the following:
- Close Claude Desktop if it was running (you might need to end the task in task manager)
- Open Claude Desktop
- Click the + sign to the left of the text field
- Hover over connectors

You should now see "DBSchenker" listed as a connector. 

Example questions:
'Can you give me the information for my DBSchenker shipment?' It should ask for your reference ID.
