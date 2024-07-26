ROUTING
--------

A modern web app uses meaningful URLS to help users.

Users more likely to like a page and come back if the page uses a meaningful URL they can remenber and use to directly visit a page.

route() decorator to bind a function to a URL.

@my_app.route("/hello")
def hello_world():
    return "<p>Hello, Makena. Welcome to Flask!</p>"

@my_app.route("/")
def indexes():
    return "Index page"

You can make parts of the URL dynamic and attach multiple rules to a function.

VARIABLE RULES
----------------
You can add variable sections to a URL by marking these sections with <var_name>.

Your function will then receive the <var_name> as a keyword argument.
You can also use a converter to specify the type of the argument.
	<converter:var_name> 
Convereter Types:
	string -> the default
	       -> any text without a slash
	int -> positive ints
	float -> positive floating point values.
	path -> like string but accepts slashes
	uuid -> accepts UUID strings.

UNIQUE URLS/ REDIRECTION BEHAVIOR
----------------------------------
# Trailing slash usage
@my_app.route("/projects/")
def show_project():
    return f"Project page"

@my_app.route("/about")
def show_about():
    return f"About page"

Canonical URL for the projects endpoint has a trailing slash.
It is like a folder in a file sysstem
If you access this URL without a trailing / -> /projects,
Flask redirects you to the canoniacal URL with the trailing slash -> /projects/

Canonical URL for about endpoint does not have a trailing /
it is like the pathname of a file.
Accessing the URL with a trailing slash ->/about/,
produces a 404 NotFound error.

Benefits: Helps keep URLS unique for these resources, thus helps search engines avoid indexing the same page twice.


URL BUILDING
-------------
Use the url_for() func to build a URL to a specific function.
Accepts the name of the function as its first arg,
and any number of keyword args, each corresponding to a variable part of the URL rule.
Unknown variable parts are appended to the URL as query parameters.
Why build URLS using the URL reversing function url_for() instead of hard coding them into the templates?
	1. Reversing is more descriptive than hard coded URLS:
		With url_for(), you reference the endpoint name, thus making your code more readable and mantainable.
	2. You can change your URLs in one go instead of needing to remember to manually change hard-coded URLs.
If you need to change a route, you only need to change it in one place (the route definition) rather than every instance where it's hard-coded.	
	3. url_for() properly escapes special characters in URLs, preventing potential errors.
	4. url_for() generates absolute URLs, preventing issues with relative paths that can arise when the current URL path changes.
	5. If your application is placed outside the URL root, for example, in /myapplication instead of /, url_for() properly handles that for you.
When deploying an application under a subdirectory, url_for() automatically adjusts URLs to include the subdirectory.

Changing Host IP Address in Flask
--------------------------------------
What is a Host Ip address:
The network address that identifies a device on a network.
For flask applications, the host ip address is the address that the application listens to for incoming requests.
By default, flask applications listen on the localhost address 127.0.0.1:5000.
This means that the flask application can only be accessed from the same machine that it is run on.

It is useful to access the application from other devices on the same network, or from the internet.
So the host ip address needs to be changed to allow the application to be accessed from other devices.
Do this by specifying the host ip address in the app.run() function of the flask application.

For example: we can use the host parameter to specify the host ip address, and the port parameter to specify the port number.

Using strict_slashes
-----------------------
In Python Flask, the strict_slashes option in route decorators controls whether a URL endpoint should strictly differentiate between URLs with and without a trailing slash. By default, Flask distinguishes between these two, treating them as separate routes. However, strict_slashes allows you to configure this behavior according to your application needs.

By default, Flask treats URLs with and without a trailing slash as distinct endpoints. For example, consider the following route definition:

@app.route('/example')
def example():
    return "This is the example endpoint"
With this configuration:

Accessing /example will work and return the expected response.
Accessing /example/ will result in a 404 Not Found error because Flask considers it a different endpoint.
Using strict_slashes=False
When strict_slashes is set to False, Flask will not differentiate between URLs with and without a trailing slash. This means that both variations of the URL will be treated as the same endpoint. Here’s how you can configure it:

@app.route('/example', strict_slashes=False)
def example():
    return "This is the example endpoint"
With this configuration:

Accessing /example will work and return the expected response.
Accessing /example/ will also work and return the same response.
