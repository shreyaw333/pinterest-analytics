import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './App.css';

const Dashboard = () => {
  const [metrics] = useState({
    categoryAccuracy: '90.9%',
    catalogCoverage: '51.3%',
    interactionTypes: '5',
    modelAccuracyLift: '9.1x'
  });

  // Engagement breakdown by interaction type from real data
  const [engagementData] = useState([
    { type: 'Save',    count: 997,  weight: 5 },
    { type: 'Like',    count: 646,  weight: 3 },
    { type: 'Click',   count: 490,  weight: 2 },
    { type: 'Share',   count: 247,  weight: 4 },
    { type: 'Comment', count: 117,  weight: 1 },
  ]);

  // Real category distribution from weighted interaction data
  const [categoryData] = useState([
    { name: 'Travel',          value: 11.2, color: '#e60023' },
    { name: 'Food',            value: 10.2, color: '#ff4081' },
    { name: 'Home Decor',      value: 10.1, color: '#9c27b0' },
    { name: 'Art',             value: 10.0, color: '#673ab7' },
    { name: 'Health & Fitness',value: 10.0, color: '#3f51b5' },
    { name: 'Photography',     value: 9.8,  color: '#2196f3' },
    { name: 'Gardening',       value: 9.8,  color: '#4caf50' },
    { name: 'DIY & Crafts',    value: 9.8,  color: '#ff9800' },
    { name: 'Fashion',         value: 9.6,  color: '#f44336' },
    { name: 'Beauty',          value: 9.3,  color: '#e91e63' },
  ]);

  // Real top pins by saves_count from dataset (titles cleaned up for readability)
  const [trendingPins] = useState([
    { title: 'Night Sky Photography Tips',    category: 'Photography', saves: '531', score: 146.1 },
    { title: 'Weekend DIY Shelf Build',       category: 'DIY & Crafts', saves: '524', score: 115.7 },
    { title: 'Minimalist Home Office Setup',  category: 'Photography', saves: '455', score: 116.0 },
    { title: 'Modern Living Room Makeover',   category: 'Home Decor',  saves: '453', score: 78.1  },
  ]);

  // Real ML model results from ml_pipeline/results/metrics.json
  const [modelMetrics] = useState([
    {
      model: 'Category Preference (RF)',
      metric: 'Accuracy',
      value: '90.9%',
      note: '5-fold CV · 9.1x lift over random baseline'
    },
    {
      model: 'Matrix Factorization (SVD)',
      metric: 'Catalog Coverage',
      value: '51.3%',
      note: '50 latent factors · 11.5% explained variance'
    },
    {
      model: 'Content-Based (TF-IDF)',
      metric: 'Coverage',
      value: '3.7%',
      note: 'Pin metadata · category + subcategory + tags'
    },
  ]);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(to right, #ef4444, #dc2626)',
        color: 'white',
        padding: '2rem 1.5rem'
      }}>
        <div style={{ maxWidth: '80rem', margin: '0 auto' }}>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
            Pinterest Recommender Dashboard
          </h1>
          <p style={{ opacity: 0.9 }}>
            ML pipeline analytics · 2,497 interactions · 2,000 users · 48,672 pins
          </p>
        </div>
      </div>

      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '2rem 1.5rem' }}>

        {/* Key Metrics */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '1.5rem',
          marginBottom: '2rem'
        }}>
          <MetricCard
            label="Category Preference Accuracy"
            value={metrics.categoryAccuracy}
            change="vs 10% random baseline"
          />
          <MetricCard
            label="SVD Catalog Coverage"
            value={metrics.catalogCoverage}
            change="of 48,672 pins covered"
          />
          <MetricCard
            label="Interaction Signal Types"
            value={metrics.interactionTypes}
            change="save · like · click · share · comment"
          />
          <MetricCard
            label="Lift Over Baseline"
            value={metrics.modelAccuracyLift}
            change="RandomForest, 5-fold CV"
          />
        </div>

        {/* Charts */}
        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          marginBottom: '2rem'
        }}>
          <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
              Interaction & Category Breakdown
            </h3>
            <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '0.25rem' }}>
              Based on 2,497 real interactions from generated dataset
            </p>
          </div>
          <div style={{ padding: '1.5rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>

              {/* Bar-style line chart for interaction counts */}
              <div>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '1rem' }}>
                  Interactions by Type (count)
                </h4>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={engagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="type" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="count"
                      stroke="#e60023"
                      strokeWidth={3}
                      name="Interaction Count"
                      dot={{ r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Pie Chart - real category distribution */}
              <div>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '1rem' }}>
                  Category Distribution (weighted interactions)
                </h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value}%`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>

        {/* Model Results + Trending Pins */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '2rem' }}>

          {/* Real ML Model Results */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
                Model Evaluation Results
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '0.25rem' }}>
                From ml_pipeline/results/metrics.json
              </p>
            </div>
            <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {modelMetrics.map((m, i) => (
                <ModelMetricCard key={i} data={m} />
              ))}
            </div>
          </div>

          {/* Trending Pins */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
                Top Trending Pins
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '0.25rem' }}>
                Ranked by saves_count from dataset
              </p>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                {trendingPins.map((pin, index) => (
                  <TrendingPinCard key={index} pin={pin} />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{ marginTop: '3rem', textAlign: 'center', color: '#6b7280', fontSize: '0.875rem' }}>
          <p>Pinterest Trending Pins Recommender · Django · React · Scikit-learn · PostgreSQL · Kafka</p>
          <p style={{ marginTop: '0.25rem' }}>
            Category preference accuracy: 90.9% · 9.1x lift over random baseline
          </p>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, change }) => (
  <div style={{
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    padding: '1.5rem',
    textAlign: 'center'
  }}>
    <div style={{ fontSize: '0.8rem', color: '#6b7280', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
      {label}
    </div>
    <div style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#e60023', marginBottom: '0.5rem' }}>
      {value}
    </div>
    <div style={{ fontSize: '0.75rem', color: '#10b981' }}>
      {change}
    </div>
  </div>
);

const ModelMetricCard = ({ data }) => (
  <div style={{ backgroundColor: '#f9fafb', borderRadius: '0.5rem', padding: '1rem' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
      <div style={{ fontWeight: '600', fontSize: '0.875rem' }}>{data.model}</div>
      <div style={{ fontWeight: 'bold', color: '#e60023', fontSize: '1.125rem' }}>{data.value}</div>
    </div>
    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>{data.note}</div>
  </div>
);

const TrendingPinCard = ({ pin }) => (
  <div style={{ backgroundColor: '#f9fafb', borderRadius: '0.5rem', padding: '1rem', textAlign: 'center' }}>
    <div style={{
      width: '100%',
      height: '5rem',
      background: 'linear-gradient(to right, #e60023, #dc2626)',
      borderRadius: '0.5rem',
      marginBottom: '0.75rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 'bold',
      fontSize: '0.75rem',
      padding: '0.25rem'
    }}>
      {pin.category.toUpperCase()}
    </div>
    <div style={{ fontSize: '0.8rem', fontWeight: '600', marginBottom: '0.5rem' }}>
      {pin.title}
    </div>
    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
      {pin.saves} saves · score {pin.score}
    </div>
  </div>
);

export default Dashboard;