import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const getCompanies = async () => {
  const response = await axios.get(`${API_BASE_URL}/companies/`);
  return response.data;
};

export const getCompanyDetail = async (symbol: string) => {
  const response = await axios.get(`${API_BASE_URL}/companies/${symbol}/`);
  return response.data;
};
