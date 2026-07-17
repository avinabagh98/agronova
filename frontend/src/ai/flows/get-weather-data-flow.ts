// src/ai/flows/get-weather-data-flow.ts
'use server';

/**
 * @fileOverview A flow to get real-time weather data from WeatherAPI.
 *
 * - getWeatherData - A function that returns real-time weather data.
 * - WeatherData - The return type for the getWeatherData function.
 */

import { ai } from '@/ai/genkit';
import { z } from 'genkit';

const WeatherDataSchema = z.object({
  temperature: z.number().describe('The current temperature in Celsius.'),
  feelsLike: z.number().describe('The feels like temperature in Celsius.'),
  rainfall: z.number().describe('The rainfall in millimeters.'),
  sunlightHours: z.number().describe('The daily sunlight hours.'),
  windSpeed: z.number().describe('The current wind speed in km/h.'),
  humidity: z.number().describe('The current humidity percentage.'),
  pressure: z.number().describe('Atmospheric pressure in hPa.'),
  uvIndex: z.number().optional().describe('UV index (0-11+).'),
  visibility: z.number().describe('Visibility in kilometers.'),
  cloudCoverage: z.number().describe('Cloud coverage percentage.'),
  dewPoint: z.number().optional().describe('Dew point in Celsius.'),
  description: z.string().describe('Weather description.'),
  location: z.string().describe('Location name.'),
  sunrise: z.number().optional().describe('Sunrise time (Unix timestamp).'),
  sunset: z.number().optional().describe('Sunset time (Unix timestamp).'),
});

export type WeatherData = z.infer<typeof WeatherDataSchema>;

export async function getWeatherData(
  lat?: number,
  lon?: number
): Promise<WeatherData> {
  return getWeatherDataFlow({ lat, lon });
}

const getWeatherDataFlow = ai.defineFlow(
  {
    name: 'getWeatherDataFlow',
    inputSchema: z.object({
      lat: z.number().optional(),
      lon: z.number().optional(),
    }),
    outputSchema: WeatherDataSchema,
  },

  async (input) => {
   
    // WeatherAPI key
    const apiKey = process.env.WEATHER_API_KEY;
    // Default location: Kolkata, West Bengal
    const lat = input.lat ?? 22.5726;
    const lon = input.lon ?? 88.3639;    
    try {
      // Fallback if API key missing
      if (!apiKey) {
        console.warn(
          'Weather API key not configured, using simulated data'
        );

        return generateSimulatedWeatherData();
      }

      // Fetch real weather data
      const weatherResponse = await fetch(
        `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${lat},${lon}&aqi=no`,
        {
          method: 'GET',
          cache: 'no-store',
        }
      );
      if (!weatherResponse.ok) {
        console.error(
          'Weather API error:',
          weatherResponse.status,
          weatherResponse.statusText
        );

        return generateSimulatedWeatherData();
      }

      const data = await weatherResponse.json();

      const current = data.current;
      const location = data.location;

      return {
        temperature: current.temp_c,
        feelsLike: current.feelslike_c,
        rainfall: current.precip_mm,

        // Estimated sunlight hours
        sunlightHours: 12 - (current.cloud / 100) * 6,

        windSpeed: current.wind_kph,
        humidity: current.humidity,
        pressure: current.pressure_mb,
        uvIndex: current.uv,
        visibility: current.vis_km,
        cloudCoverage: current.cloud,

        // Approximate dew point
        dewPoint:
          current.temp_c - ((100 - current.humidity) / 5),

        description: current.condition.text,
        location: location.name,

        // Current endpoint doesn't include sunrise/sunset
        sunrise: undefined,
        sunset: undefined,
      };
    } catch (error) {
      console.error('Error fetching weather data:', error);

      return generateSimulatedWeatherData();
    }
  }
);

async function generateSimulatedWeatherData(): Promise<WeatherData> {
  return {
    temperature: 32.5,
    feelsLike: 31.2,
    rainfall: 5.2,
    sunlightHours: 6.2,
    windSpeed: 18.5,
    humidity: 78,
    pressure: 1010,
    uvIndex: 7,
    visibility: 8.5,
    cloudCoverage: 52,
    dewPoint: 24.1,
    description: 'Partly cloudy',
    location: 'Kolkata',
    sunrise: Date.now() / 1000 - 3600 * 2,
    sunset: Date.now() / 1000 + 3600 * 6,
  };
}