import Head from 'next/head';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/jobs/`, {
        params: { limit: 10 }
      });
      setJobs(response.data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>CareerHunter AI - Find Your Dream Job</title>
        <meta name="description" content="AI-powered job discovery platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              CareerHunter AI
            </h1>
            <p className="mt-2 text-gray-600">
              Discover your next career opportunity with AI-powered job matching
            </p>
          </div>
        </header>

        <main className="max-w-7xl mx-auto py-12 sm:px-6 lg:px-8">
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full border-4 border-t-blue-500"></div>
              <p className="mt-4">Loading jobs...</p>
            </div>
          ) : jobs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No jobs found. Try adjusting your search.</p>
            </div>
          ) : (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-gray-900">
                Featured Jobs
              </h2>
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {jobs.map((job) => (
                  <div key={job.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
                    <div className="p-6">
                      <h3 className="text-lg font-medium text-gray-900">{job.title}</h3>
                      <p className="mt-2 text-sm text-gray-500">
                        {job.company?.name || 'Company Name'}
                      </p>
                      <p className="mt-1 text-sm text-gray-600">
                        {job.location || 'Location not specified'}
                      </p>
                      {job.salary_min && job.salary_max && (
                        <p className="mt-2 text-sm font-medium text-green-600">
                          ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                        </p>
                      )}
                      <a href={job.application_url} target="_blank" rel="noopener noreferrer"
                        className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                        Apply Now
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>

        <footer className="bg-white border-t">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} CareerHunter AI. All rights reserved.
            </p>
          </div>
        </footer>
      </div>
    </>
  );
}
