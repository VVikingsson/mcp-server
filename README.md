# DB Schenker Shipment Information MCP Server

Dear Sendify!
I met you(r Erik) at the Gösta career fair and was intrigued by what seemed like a great place to work and grow. Of course, I decided to apply to the summer internship but then I found this opportunity for fast-tracking the application, so here I am!

## My journey and approach

### Understanding MCP:
I had never heard of MCP prior to this, so I started by visiting their documentation. A skill I've developed during my studies is how to use LLMs to improve my learning (as opposed to impede - the trap which many students fall in), so I also asked lots of questions asking for pedagogical explanations. Whenever something didn't quite feel intuitive or right, it was of course important to fact check the robot. Since I've studied network protocols, understanding MCP was rather intuitive.

### Learning Web Scraping:
Automating website interaction is something I've had in mind for some projects that only ever stayed in my head, but with this I had no choice but to learn it. At first, I thought I would be parsing HTML using a simple request library but, of course, someone has always had the same problem as you have and there exists a good library for most things. My approach to selecting a library to use was to describe the use case to an LLM and then ask it for suggestions with provided rationale. I got recommended Playwright, a library for automating web tests, and after looking into it for some time I decided to stick with it. In essence, it launches a headless browser and provides an intuitive way for you as a programmer to navigate it.

## How to test it yourself (with Claude Desktop)
1. [Install uv for your OS](https://docs.astral.sh/uv/getting-started/installation/)
2. Run commands to clone repository and install dependencies
```
git clone https://github.com/VVikingsson/mcp-server.git
cd mcp-server/dbschenker_server
uv sync
```
3. Set up Claude Desktop
   - [Download Claude Desktop for your OS](https://claude.com/download) (if you don't already have it)
   - Follow the installation instructions and open the app.
   - Now in the app, click the hamburger menu in the top left.
   - Navigate to File -> Settings -> Developer.
   - Click 'Edit Config'.
   - Add the following, then save the file:
```
  {
  "mcpServers": {
    "DBSchenker": {
      "command": "uv", // If this does not work, swap it out for the full path to uv.exe. Use 'where uv' in a terminal to find location.
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\dbschenker_server",
        "run",
        "mcp_server.py"
      ]
    }
  }
}
```
4. Verify setup
   - Close Claude Desktop if it was running (you might need to end the task a task manager)
   - Open Claude Desktop
   - Click the + sign to the left of the text field
   - Hover over connectors
   - You should not see "DBSchenker" listed as a connector.

You are now ready to test the server! Here are some example prompts:

- Example prompts
- Go
- Here
