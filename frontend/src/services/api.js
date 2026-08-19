import axios from 'axios';

// Base API configuration (Direct or Proxied)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

/**
 * Healthcheck API call
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/healthcheck');
    return response.data;
  } catch (error) {
    console.error('Healthcheck failed:', error);
    throw error;
  }
};

/**
 * Single Transaction Inference API call
 * @param {Object} payload 
 */
export const predictSingleTransaction = async (payload) => {
  try {
    const response = await api.post('/predict', payload);
    return response.data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
};

/**
 * Batch CSV Upload Inference API call
 * @param {File} file 
 */
export const predictCsvBatch = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/predict/csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('CSV batch prediction error:', error);
    throw error;
  }
};

/**
 * Fetch Model Metadata & Ablation Results
 */
export const getModelMetadata = async () => {
  try {
    const response = await api.get('/model/metadata');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch model metadata:', error);
    throw error;
  }
};

/**
 * Fetch Preset Edge Case Details
 * @param {number} caseId 
 */
export const getPresetCase = async (caseId) => {
  try {
    const response = await api.get(`/examples/${caseId}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch preset ${caseId}:`, error);
    throw error;
  }
};

export default api;
