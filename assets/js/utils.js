function isProduction() {
    return window.location.hostname.indexOf("<service_name>") != -1;
}