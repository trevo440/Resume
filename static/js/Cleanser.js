export class Cleanser {
    ensureGptFormat(text) {
        return text
            .replace(/```(?:json|python)?/g, '')
            .replace(/```/g, '')              
            .replace(/'/g, '"')
            .trim()
            .split('=').pop().trim() || '';
    }

    noQuote(text) {
        return text.replace(/['"]/g, "");
    }

    validateSchema(inputString, schema) {
        try {
            const data = JSON.parse(inputString);

            function validateObject(obj, schema) {
                if (typeof obj !== "object" || obj === null) return false;
                for (const key in schema) {
                    if (!(key in obj)) return false;

                    const expectedType = schema[key];
                    const actualValue = obj[key];

                    if (expectedType === "string" && typeof actualValue !== "string") return false;
                    if (expectedType === "array" && !Array.isArray(actualValue)) return false;
                    if (typeof expectedType === "object" && !validateObject(actualValue, expectedType)) return false;
                }
                return true;
            }

            return validateObject(data, schema);
        } catch (error) {
            return false;
        }
    }
}


