import React, { useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { Button, Input, message, Upload } from 'antd';
import type { RcFile, UploadFile, UploadProps } from 'antd/es/upload/interface';
import { basePath } from '../../providers/env';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface UploadResponse {
    id: string;
}

export const Uploader: React.FC = () => {
    const navigate = useNavigate();
    const [fileList, setFileList] = useState<UploadFile[]>([]);
    const [uploading, setUploading] = useState(false);
    const [goldanName, setGoldanName] = useState('');

    const handleUpload = () => {
        const formData = new FormData();
        fileList.forEach((file) => {
            formData.append('files', file as RcFile);
        });
        formData.append('goldanName', goldanName);
        console.log('Uploading files', fileList);
        setUploading(true);

        axios.post<UploadResponse>(basePath + '/api/v1/upload/files', formData)
            .then((response) => {
                setFileList([]);
                message.success('Загрузка завершена.');
                navigate('/result/' + response.data.id);
            })
            .catch(() => {
                message.error('Загрузка не удалась.');
            })
            .finally(() => {
                setUploading(false);
            });
    };

    const props: UploadProps = {
        onRemove: (file) => {
            const index = fileList.indexOf(file);
            const newFileList = fileList.slice();
            newFileList.splice(index, 1);
            setFileList(newFileList);
        },
        beforeUpload: (file) => {
            setFileList((prev) => [...prev, file]);

            return false;
        },
        fileList,
        accept: '.pdf,.zip,.rar,.7z',
        multiple: true,
    };

    return (
        <>
            <Input placeholder="Эталонное название" value={goldanName} onChange={(e) => setGoldanName(e.target.value)} />
            <br />
            <br />

            <Upload.Dragger {...props}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">Кликните или перетащите файлы в эту область для загрузки</p>
                <p className="ant-upload-hint">
                    Поддержка одиночной или массовой загрузки.
                    Разрешенные форматы: .pdf или .zip, .rar, .7z (с файлами .pdf внутри).
                </p>
            </Upload.Dragger>
            <Button
                type="primary"
                onClick={handleUpload}
                disabled={fileList.length === 0}
                loading={uploading}
                style={{ marginTop: 16 }}
            >
                {uploading ? 'Загрузка...' : 'Начать загрузку'}
            </Button>
        </>
    );
};