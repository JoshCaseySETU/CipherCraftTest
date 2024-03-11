function encryptHieroglyphic(message) {
    // Create a mapping of characters to hieroglyphic symbols
    const hieroglyphicMapping = {
        'A': '𓃀',
        'B': '𓂋',
        'C': '𓅱',
        'D': '𓀀',
        'E': '𓀭',
        'F': '𓀾',
        'G': '𓁹',
        'H': '𓆱',
        'I': '𓍯',
        'J': '𓃾',
        'K': '𓆛',
        'L': '𓂧',
        'M': '𓇌',
        'N': '𓆑',
        'O': '𓁨',
        'P': '𓈖',
        'Q': '𓄿',
        'R': '𓅓',
        'S': '𓂋',
        'T': '𓏏',
        'U': '𓃭',
        'V': '𓀓',
        'W': '𓀭𓁷',
        'X': '𓏭',
        'Y': '𓀠',
        'Z': '𓆱',
        ' ': ' ',
    };

    // Convert the message to uppercase for simplicity
    message = message.toUpperCase();

    // Initialize an empty string to store the encrypted message
    let encryptedMessage = '';

    // Iterate through each character in the message
    for (let i = 0; i < message.length; i++) {
        const char = message[i];
        
        // Check if the character exists in the mapping
        if (hieroglyphicMapping.hasOwnProperty(char)) {
            // If yes, append the corresponding hieroglyphic symbol to the encrypted message
            encryptedMessage += hieroglyphicMapping[char];
        } else {
            // If not, keep the character unchanged
            encryptedMessage += char;
        }
    }

    // Return the encrypted message
    return encryptedMessage;
}


