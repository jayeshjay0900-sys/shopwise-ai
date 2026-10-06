import axios from 'axios';
import { SearchRequest, SearchResponse } from './types';

// Use relative URL - works for both local and production
const API_BASE_URL = '';

export const api = {
  async search(query: string): Promise<SearchResponse> {
    const response = await axios.post<SearchResponse>(
      `${API_BASE_URL}/search`,
      { query } as SearchRequest
    );
    return response.data;
  },

  async health(): Promise<any> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },
};
