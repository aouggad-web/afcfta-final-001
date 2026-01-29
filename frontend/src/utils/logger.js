/**
 * Centralized error logging utility
 * Provides consistent error handling and logging across the application
 */

/**
 * Log an error with context
 * @param {string} context - Context where the error occurred (e.g., "API Call", "Data Loading")
 * @param {Error|string} error - The error object or message
 * @param {object} additionalInfo - Optional additional information to log
 */
export const logError = (context, error, additionalInfo = {}) => {
  const errorMessage = error instanceof Error ? error.message : error;
  const errorStack = error instanceof Error ? error.stack : undefined;
  
  console.error(`[${context}] Error:`, errorMessage);
  
  if (errorStack && process.env.NODE_ENV === 'development') {
    console.error('Stack trace:', errorStack);
  }
  
  if (Object.keys(additionalInfo).length > 0) {
    console.error('Additional info:', additionalInfo);
  }
};

/**
 * Log a warning
 * @param {string} context - Context where the warning occurred
 * @param {string} message - Warning message
 */
export const logWarning = (context, message) => {
  console.warn(`[${context}] Warning:`, message);
};

/**
 * Log info message (only in development)
 * @param {string} context - Context 
 * @param {string} message - Info message
 */
export const logInfo = (context, message) => {
  if (process.env.NODE_ENV === 'development') {
    console.log(`[${context}] Info:`, message);
  }
};
