'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface Field {
  _id: string;
  name: string;
  location: string;
  crop: string;
  size: number;
  coordinates: [number, number][];
  color: string;
  createdAt: string;
}

interface FieldsContextType {
  fields: Field[];
  addField: (field: Field) => void;
  updateField: (id: string, updates: Partial<Field>) => void;
  deleteField: (id: string) => void;
  getFieldById: (id: string) => Field | undefined;
}

const FieldsContext = createContext<FieldsContextType | undefined>(undefined);

export function FieldsProvider({ children }: { children: ReactNode }) {
  const [fields, setFields] = useState<Field[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load fields from API on mount
  useEffect(() => {
    const fetchFields = async () => {
      try {
        const response = await fetch('/api/fields');
        if (response.ok) {
          const data = await response.json();
          setFields(data);
        }
      } catch (error) {
        console.error('Error loading fields:', error);
      } finally {
        setIsLoaded(true);
      }
    };
    fetchFields();
  }, []);

  const addField = async (field: Omit<Field, '_id'>) => {
    try {
      const response = await fetch('/api/fields', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(field),
      });
      if (response.ok) {
        const newField = await response.json();
        setFields(prev => [newField, ...prev]);
      }
    } catch (error) {
      console.error('Error adding field:', error);
    }
  };

  const updateField = async (id: string, updates: Partial<Field>) => {
    try {
      const response = await fetch(`/api/fields/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      });
      if (response.ok) {
        const updatedField = await response.json();
        setFields(prev => prev.map(field => 
          field._id === id ? updatedField : field
        ));
      }
    } catch (error) {
      console.error('Error updating field:', error);
    }
  };

  const deleteField = async (id: string) => {
    try {
      const response = await fetch(`/api/fields/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        setFields(prev => prev.filter(field => field._id !== id));
      }
    } catch (error) {
      console.error('Error deleting field:', error);
    }
  };

  const getFieldById = (id: string) => {
    return fields.find(field => field._id === id);
  };


  return (
    <FieldsContext.Provider value={{ fields, addField, updateField, deleteField, getFieldById }}>
      {children}
    </FieldsContext.Provider>
  );
}

export function useFields() {
  const context = useContext(FieldsContext);
  if (context === undefined) {
    throw new Error('useFields must be used within a FieldsProvider');
  }
  return context;
}
