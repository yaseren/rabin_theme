app_name = "rabin_theme"
app_title = "Rabin ERPNext Theme"
app_publisher = "Rabin"
app_description = "Modern, Persian-friendly RTL styling for Frappe Desk"
app_email = ""
app_license = "MIT"

# Keep the theme isolated from Frappe and ERPNext core files.
# These assets are served from /assets/rabin_theme/ after `bench build`.
app_include_css = [
    "/assets/rabin_theme/css/rabin_theme.css",
    "/assets/rabin_theme/css/rabin_rtl.css",
]
