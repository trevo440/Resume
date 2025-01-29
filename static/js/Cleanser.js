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
}

