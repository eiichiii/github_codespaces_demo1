import React, { useState } from 'react';

function App() {
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults([]);
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    try {
      // 仮のAPIエンドポイント
      const res = await fetch('/api/count', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('APIエラー');
      const data = await res.json();
      setResults(data.results);
    } catch (err) {
      setError('集計に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>LOC/eLOC カウンター</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          multiple
          webkitdirectory="true"
          directory="true"
          onChange={handleFileChange}
        />
        <button type="submit" disabled={loading || files.length === 0}>
          {loading ? '集計中...' : '集計する'}
        </button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {results.length > 0 && (
        <table border="1" cellPadding="6" style={{ marginTop: 20, width: '100%' }}>
          <thead>
            <tr>
              <th>ファイル名</th>
              <th>LOC</th>
              <th>eLOC</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, i) => (
              <tr key={i}>
                <td>{r.path}</td>
                <td>{r.loc}</td>
                <td>{r.eloc}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
