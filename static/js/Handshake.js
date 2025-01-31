// Fetch config from the global scope (set in index.html)
const clientUUID = window.appConfig.clientUUID;
const csrfToken = window.appConfig.csrfToken;

/**
 * Cleans input data by:
 * - Removing empty, null, or undefined values
 * - Ensuring only valid JSON is sent
 */
function cleanData(data) {
    if (typeof data !== "object" || data === null) return {}; // Ensure it's an object
    return Object.fromEntries(
        Object.entries(data).filter(([_, value]) => value !== null && value !== undefined && value !== "")
    );
}

/**
 * Makes an API request with authentication headers, input validation, and error handling.
 * - Includes a 10-second timeout for network reliability.
 * - Returns sanitized JSON responses or errors.
 */
export async function apiRequest(url, method = "GET", body = null) {
    const headers = {
        "Content-Type": "application/json",
        "X-Client-UUID": clientUUID,
        "X-CSRF-Token": csrfToken
    };

    const options = { method, headers };
    if (body) options.body = JSON.stringify(cleanData(body));

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout
    options.signal = controller.signal;

    try {
        const response = await fetch(url, options);
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("API Request Failed:", error.message);
        return { status: "error", message: error.message };
    }
}


    
