import { DislikeOutlined, LikeOutlined } from '@ant-design/icons';
import { AutoComplete, Button, Card, Divider, Form, Input, List, Segmented, Select, Spin, Typography, message } from 'antd';
import axios from 'axios';
import { basePath } from '../providers/env';
import { useCallback, useEffect, useState } from 'react';
import "react-multi-carousel/lib/styles.css";

import debounce from 'lodash.debounce';
import Carousel from 'react-multi-carousel';
import { useNavigate } from 'react-router-dom';

export const selectedTypeOptions = [
    {
        value: 'cosmetic',
        label: 'Косметика',
    },
    {
        value: 'super',
        label: 'Супермаркет',
    },
]

interface ProductsGet {
    item_id: number;
    name: string;
    type: string;
}

interface ProductsGetExtended extends ProductsGet {
    value: number;
    label: JSX.Element | string;
}

const renderItem = (item: ProductsGet): ProductsGetExtended => ({
    ...item,
    value: item.item_id,
    label: (
        <div
            style={{
                display: 'flex',
                justifyContent: 'space-between',
            }}
        >
            {item.name}
        </div>
    ),
});

export const Products = (): JSX.Element => {
    const [deviceOptions, setDeviceOptions] = useState<number[]>([]);
    const [deviceIsLoading, setDeviceIsLoading] = useState<boolean>(false);
    const [selectedType, setSelectedType] = useState<string | number>(selectedTypeOptions[0].value);
    const [deviceQuery, setDeviceQuery] = useState<string>('');

    const navigate = useNavigate();

    const handleChangeSelectedType = (value: string | number) => {
        setSelectedType(value);
    };


    const handleSearch = (value: string, type: string) => {
        setDeviceOptions([]);
        if (!value) return;
        setDeviceIsLoading(true);
        axios.get<number[]>(basePath + '/api/v1/matching/devices', { params: { id: value, type } })
            .then((response) => {
                console.log(response.data)
                setDeviceOptions(response.data);
            })
            .catch(() => {
                message.error('Загрузка данных не удалась.');
            })
            .finally(() => {
                setDeviceIsLoading(false);
            });
    };

    const debouncedSearchHandler = useCallback(
        debounce(handleSearch, 550)
        , []);

    const onSearch = (searchText: string, props: { type: string }) => {
        console.log('onSearch', searchText, props.type);
        if (!/^[0-9]*$/.test(searchText)) return;
        setDeviceQuery(searchText);
        debouncedSearchHandler(searchText, props.type);
    };

    const onSelect = (_: string, item: { value: number, title: string }) => {
        console.log('onSelect', item.value);
        setDeviceQuery(String(item.value));
        setDeviceOptions([]);
    };


    const onFinish = ({ type, device_id }: { type: string, device_id: number }) => {
        navigate(`/products/${type}/${device_id}`);
    };

    const [form] = Form.useForm();


    useEffect(() => {
        // form.setFieldsValue({ device_id: '' });
        form.setFieldValue('device_id', '');
    }, [selectedType]);



    return (
        <>
            <h1>Товары</h1>
            <Form
                form={form}
                name="basic"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 16 }}
                style={{ maxWidth: 600 }}
                initialValues={{ remember: true }}
                onFinish={onFinish}
                autoComplete="off"
            >
                <Form.Item
                    label="Тип"
                    name="type"
                    rules={[{ required: true, message: 'Выберите тип' }]}
                    initialValue={selectedTypeOptions[0].value}
                >
                    <Segmented options={selectedTypeOptions}
                        value={selectedType}

                        onChange={handleChangeSelectedType}
                    />
                </Form.Item>

                <Form.Item
                    label="ID заведения"
                    name="device_id"
                    rules={[{ required: true, message: 'Введите ID заведения' }]}
                    dependencies={['type']}
                >
                    <Select
                        filterOption={false}
                        showSearch
                        options={deviceOptions.map((id) => ({ value: id, title: String(id) }))} loading={deviceIsLoading}
                        onSearch={(value: string) => {
                            return onSearch(value, form.getFieldsValue());
                        }}
                        value={deviceQuery}
                        onSelect={onSelect}
                        onClear={() => {
                            setDeviceQuery('');
                        }}
                        allowClear
                        dropdownStyle={{ minWidth: 200 }}
                        style={{ minWidth: 150 }}
                        notFoundContent={
                            <div style={{ textAlign: 'center' }}>{deviceIsLoading ? <Spin size="small" /> : <Typography.Text type='secondary'>Ничего не найдено</Typography.Text>}
                            </div>}
                    // disabled={!!deviceQuery}
                    />
                </Form.Item>
                <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                    <Button type="primary" htmlType="submit">
                        Продолжить
                    </Button>
                </Form.Item>
            </Form>
            {/* <Typography.Text>Тип:{' '}</Typography.Text>
            <Segmented options={selectedTypeOptions}
                value={selectedType}
                onChange={handleChangeSelectedType}
            // disabled={selectedItems.length > 0} 
            />
            <br />
            {selectedType} {deviceQuery}
            <br />
            <Typography.Text>ID заведения:{' '}</Typography.Text>
            <Select
                filterOption={false}
                showSearch
                options={deviceOptions.map((id) => ({ value: id, label: String(id) }))} loading={deviceIsLoading}
                onSearch={changeQueryDevice}
                value={deviceQuery}
                // onChange={(value) => debounceFetcher(value)}
                onSelect={handleSelectDevice}
                onClear={() => {
                    setDeviceQuery('');
                    setDeviceSelected(false);
                }}
                allowClear
                dropdownStyle={{ minWidth: 200 }}
                style={{ minWidth: 150 }}
                notFoundContent={
                    <div style={{ textAlign: 'center' }}>{deviceIsLoading ? <Spin size="small" /> : <Typography.Text type='secondary'>Ничего не найдено</Typography.Text>}
                    </div>}
            // disabled={!!deviceQuery}
            /> */}

        </>
    )
};
