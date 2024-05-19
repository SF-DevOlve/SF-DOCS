import requests
import dns.resolver
from urllib.parse import urlparse

def format_domain(domain: str) -> str:
    # Remove "https://" if present
    domain = domain.replace("https://", "")
    # Remove "http://" if present
    domain = domain.replace("http://", "")
    # Remove any path after domain
    domain = domain.split("/")[0]
    # Add "www" if not present
    if not domain.startswith("www."):
        domain = "www." + domain
    return domain



def api_dns_resolution(domain):
    """
    Resolves the IP address of a given domain using the Google DNS service.

    Args:
        domain (str): The domain name to resolve.

    Returns:
        str: The IP address of the domain if successful, None otherwise.
    """
    try:
        domain = format_domain(domain)
        response = requests.get(f"https://dns.google/resolve?name={domain}")
        if response.status_code == 200:
            data = response.json()
            ip_address = data['Answer'][0]['data']
            return ip_address
        else:
            return False
    except requests.RequestException:
        return False

def check_phishing_dns(url, local_dns_resolution,number_=12):
    """
    Checks if a given URL is likely to be a phishing attempt.

    Args:
        url (str): The URL to be checked.
        local_dns_resolution (str): The local DNS resolution IP address.

    Returns:
        None

    Prints:
        - If the local IP and API IP match, it prints that the URL is likely not phishing.
        - If the local IP and API IP don't match or there was an error in resolution, it prints that the URL might be phishing or there was an error in resolution.
    """
    try:
        domain = format_domain(url)  # Extract domain from URL
        local_ip = local_dns_resolution
        for i in range(number_):
            api_ip = api_dns_resolution(domain)
            if local_ip and api_ip and local_ip == api_ip:
                return True
        return False
    except Exception as e:
        return False
if __name__ == "__main__":
    # url = input("Enter the URL to check for phishing: ")
    ip=api_dns_resolution(format_domain("www.google.com"))
    print(ip)
    print(check_phishing_dns("www.google.com",ip))
    




