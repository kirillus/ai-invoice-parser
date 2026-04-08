import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const onDrop = useCallback((acceptedFiles, fileRejections) => {
    if (fileRejections.length > 0) {
      const firstRejection = fileRejections[0];
      const firstError = firstRejection.errors[0]?.message || 'File was rejected';
      setError(firstError);
      setFile(null);
      return;
    }

    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError('');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpeg', '.jpg'],
      'image/tiff': ['.tiff'],
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleUpload = async () => {
    if (file && onUpload) {
      await onUpload(file);
    }
  };

  return (
    <div className='space-y-4'>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded rounded-lg p-12 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          `}
      >
        <input {...getInputProps()} />
        {file ?
          <p className='text-gray-700'>
            {file.name} ({(file.size / 1024).toFixed(1)} KB)
          </p>
        : isDragActive ?
          <p className='text-blue-500'>Drop your invoice here...</p>
        : <p className='text-gray-400'>Drag & drop an invoice, or click to browse</p>}
      </div>
      {error && <p className='text-sm text-red-600'>{error}</p>}

      {file && (
        <button onClick={handleUpload} className='w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700'>
          Upload & Parse
        </button>
      )}
    </div>
  );
}
