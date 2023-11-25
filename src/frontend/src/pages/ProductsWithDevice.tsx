import { DislikeOutlined, LikeOutlined } from '@ant-design/icons';
import { AutoComplete, Card, Divider, Form, Input, List, Segmented, Select, Space, Spin, Tag, Tooltip, Typography, message } from 'antd';
import axios from 'axios';
import { basePath } from '../providers/env';
import { useCallback, useEffect, useState } from 'react';
import "react-multi-carousel/lib/styles.css";

import debounce from 'lodash.debounce';
import Carousel from 'react-multi-carousel';
import { useParams } from 'react-router-dom';
import { selectedTypeOptions } from './Products';
import { ICartInfo } from '../components/CartInfo/CartInfo';

import unknownBoxes from '../boxes.jpg';


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

export const ProductsWithDevice = (): JSX.Element => {
    const [options, setOptions] = useState<ProductsGetExtended[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [selectedItems, setSelectedItems] = useState<ProductsGet[]>([]);
    const [searchString, setSearchString] = useState<string>('');

    const { selectedType, deviceId } = useParams();
    const [predictedData, setPredictedData] = useState<ICartInfo>();


    const handleSearch = (value: string) => {
        console.log('Received values of form:', value, 'selectedType', selectedType, 'selectedDeviceId', deviceId);
        console.log('Received values of form:', value, 'selectedType', selectedType, 'selectedDeviceId', deviceId);
        setOptions([]);
        if (!value) return;
        setIsLoading(true);
        axios.get<ProductsGet[]>(basePath + '/api/v1/matching/find_by_name', {
            params: { q: value, type: selectedType, device_id: deviceId }
        })
            .then((response) => {
                console.log(response.data)
                setOptions(response.data.map(renderItem));
            })
            .catch(() => {
                message.error('Загрузка не удалась.');
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    const debouncedSearchHandler = useCallback(
        debounce(handleSearch, 550)
        , []);

    const onSearch = (searchText: string) => {
        setSearchString(searchText);
        debouncedSearchHandler(searchText);
    };

    const onSelect = (_: string, option: ProductsGet) => {
        console.log('onSelect', option);
        setSearchString('');
        setOptions([]);
        setSelectedItems([...selectedItems, option]);
    };

    const removeItem = (item: ProductsGet) => {
        setSelectedItems(selectedItems.filter((i) => i.item_id !== item.item_id));
    };

    const getPredict = () => {
        axios.post<ICartInfo>(basePath + '/api/v1/matching/cart_predict', selectedItems.map((i) => i.item_id), {
            params: { type: selectedType, device_id: deviceId }
        })
            .then((response) => {
                console.log(response.data)
                setPredictedData(response.data);
            })
            .catch(() => {
                message.error('Загрузка не удалась.');
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    useEffect(() => {
        if (selectedItems.length > 0) {
            getPredict();
        } else {
            setPredictedData(undefined);
        }
    }, [selectedItems]);

    return (
        <>
            <h1>Поиск товаров</h1>
            <h3>Точка №{deviceId} ({
                selectedTypeOptions.find((i) => i.value === selectedType)?.label
            })</h3>
            <br />
            <span>
                Воспользуйтесь поиском, чтобы добавить товары в корзину.
            </span>
            <br />
            <br />
            <AutoComplete
                style={{ width: 500 }}
                options={options}
                onSearch={onSearch}
                onSelect={onSelect}
                notFoundContent={
                    <div style={{ textAlign: 'center' }}>{isLoading ? <Spin size="small" /> : <Typography.Text type='secondary'>Ничего не найдено</Typography.Text>}
                    </div>}
                value={searchString}
            >
                <Input.Search size="large" placeholder="Название или id товара" enterButton loading={isLoading} />
            </AutoComplete>

            {selectedItems.length > 0 && (
                <>
                    <br />
                    <br />
                    <br />
                    <Divider>Выбранные товары</Divider>
                    <List
                        bordered
                        dataSource={selectedItems}
                        renderItem={(item) => (
                            <List.Item actions={[<a onClick={() => removeItem(item)}>Убрать</a>]}>
                                <Typography.Text>{item.name}</Typography.Text>
                            </List.Item>
                        )}
                    />
                    <br />
                </>
            )}
            <br />
            <br />
            {selectedItems.length > 0 && predictedData &&
                <>
                    <Divider>Рекомендации</Divider>
                    <br />
                    <Carousel
                        additionalTransfrom={0}
                        // arrows
                        autoPlay
                        autoPlaySpeed={3500}
                        draggable
                        focusOnSelect={false}
                        infinite={false}
                        // itemClass=""
                        keyBoardControl
                        // minimumTouchDrag={80}
                        pauseOnHover
                        renderArrowsWhenDisabled={false}
                        renderButtonGroupOutside={false}
                        renderDotsOutside={false}
                        responsive={{
                            superLargeDesktop: {
                                breakpoint: { max: 4000, min: 3000 },
                                items: 5,
                                partialVisibilityGutter: 40,
                            },
                            desktop: {
                                breakpoint: { max: 3000, min: 1700 },
                                items: 4,
                                partialVisibilityGutter: 30,
                            },
                            desktopMini: {
                                breakpoint: { max: 1700, min: 1024 },
                                partialVisibilityGutter: 30,
                                items: 3,
                            },
                            tablet: {
                                breakpoint: { max: 1024, min: 624 },
                                items: 2
                            },
                            mobile: {
                                breakpoint: { max: 624, min: 0 },
                                items: 1
                            }
                        }}
                        slidesToSlide={2}
                    // swipeable
                    >
                        <Card
                            hoverable
                            style={{ minWidth: 150, }}
                            cover={<img alt="Изображение товара"
                                width="150" height="200"
                                src={predictedData.category_url
                                    ? predictedData.category_url
                                    : unknownBoxes} onError={({ currentTarget }) => {
                                        currentTarget.onerror = null; // prevents looping
                                        currentTarget.src = unknownBoxes;
                                    }} />}
                        >
                            <Card.Meta
                                title={
                                    <Tooltip title={predictedData.name}><div style={{
                                        whiteSpace: 'pre-line',
                                    }}>{predictedData.name}</div></Tooltip>}
                                description={<Space direction="horizontal" split={'  '}>
                                    <div>Артикул: {predictedData.item_id}</div>
                                    <div>Цена: {predictedData.price}₽</div>
                                    <Tooltip title={'Категория: ' + predictedData.category_noun}>
                                        <Tag color="volcano">{predictedData.category_noun}</Tag>
                                    </Tooltip>
                                </Space>}
                            />
                        </Card>
                    </Carousel>
                    <br />
                </>
            }
        </>
    )
};
