import { MapPage } from '@/components/agrivision/MapPage';
import { Suspense } from 'react';

export default function Map() {
  return (
    <Suspense>
      <MapPage />
    </Suspense>
  );
}