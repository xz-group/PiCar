echo "Opening PiCar documentation (_build/html/index.html) ..."
{
firefox _build/html/index.html & &>/dev/null && echo "Docs opened in Firefox."
} || {
google-chrome _build/html/index.html & &>/dev/null && echo "Docs opened in Chrome." 
} || {
echo "ERROR: Please check your Firefox or Google Chrome installation."
}
