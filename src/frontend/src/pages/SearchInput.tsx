import { Alert, AutoComplete, Avatar, Badge, Button, Card, Col, Image, Form, Input, List, Row, Space, Spin, Tag, Tooltip, Typography, message } from 'antd';
import { createElement, useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ICardInfoById, ICartInfo } from '../components/CartInfo/CartInfo';
import axios from 'axios';
import { basePath } from '../providers/env';
import Meta from 'antd/es/card/Meta';
import debounce from 'lodash.debounce';
import { CheckCircleTwoTone, CloseCircleTwoTone, LikeOutlined, MessageOutlined, QuestionOutlined, StarOutlined } from '@ant-design/icons';

import unknownLogoGroup from '../unknow_item.webp';
import unknownBoxes from '../boxes.jpg';
import Search from 'antd/es/input/Search';
// import { newColorFind } from './colors';
import { lighten, modularScale } from 'polished'

const { Text } = Typography;


interface VideoInfo {
    id: string;
    source_video_title: string;
    source_channel_title: string;
    v_category: string;
    v_channel_type: string;
    badgeColor?: string;
}

interface SearchVideoResult {
    status: 'ok';
    query: string;
    data: VideoInfo[];
    count: number;
    backfill: VideoInfo[];
}

const IconText = ({ icon, text }: { icon: React.FC; text: string }) => (
    <Space>
        {createElement(icon)}
        {text}
    </Space>
);


const colorMap: Record<string, string> = {};
const selectedColors: Record<string, boolean> = {};

const generateColor = () => {
    let randomColorString = "#";
    const arrayOfColorFunctions = "0123456789abcdef";
    for (let x = 0; x < 6; x++) {
        const index = Math.floor(Math.random() * 16);
        const value = arrayOfColorFunctions[index];

        randomColorString += value;
    }
    return randomColorString;
};

const newColorFind = (id: any) => {
    // If already generated and assigned, return
    if (colorMap[id]) return colorMap[id];

    // Generate new random color
    let newColor;

    do {
        newColor = generateColor();
    } while (selectedColors[newColor]);

    // Found a new random, unassigned color
    colorMap[id] = newColor;
    selectedColors[newColor] = true;

    // Return next new color
    return newColor;
}

export const SearchInput = (): JSX.Element => {
    const navigate = useNavigate();

    const [isLoading, setIsLoading] = useState<boolean>(false);

    const [searchResult, setSearchResult] = useState<SearchVideoResult>();
    const [requestTime, setRequestTime] = useState<number>(0.0);
    const [searchString, setSearchString] = useState<string>('');


    const onSearch = () => {
        setIsLoading(true);
        axios.get<SearchVideoResult>(basePath + '/api/v1/items/info', { params: { q: searchString }, headers: { 'X-Process-Time': '0' }, },)
            .then((response) => {
                setRequestTime(parseFloat(response?.headers?.['x-process-time'] || 0));
                setSearchResult(response.data);

            })

            .catch((error) => {
                message.error('Загрузка не удалась.', error);
                console.log(error);
            })
            .finally(() => {
                setIsLoading(false);
            });
    }

    return (
        <>
            <h1>Поиск</h1>
            <Search
                placeholder="Поиск по видео"
                enterButton="Найти"
                size="large"
                onChange={(event) => setSearchString(event.target.value)}
                value={searchString}
                onSearch={onSearch}
            />
            <br />
            <br />
            <br />
            {searchResult?.data && searchResult?.data.length > 0 &&
                <List
                    dataSource={searchResult?.data}
                    loading={isLoading}
                    header='Результаты поиска'
                    locale={{ emptyText: 'Нет данных' }}
                    renderItem={(item) => (
                        <List.Item key={item.id}>
                            <List.Item.Meta
                                avatar={<Avatar style={{ backgroundColor: lighten(0.2, newColorFind(item.source_channel_title)) }}>{item.source_channel_title[0] + item.source_channel_title[1].toUpperCase()}</Avatar>}
                                title={<a>{item.source_video_title}</a>}
                                description={item.source_channel_title}
                            />
                            <div>
                                <Badge
                                    className="site-badge-count-109"
                                    count={item.v_category}
                                    style={{ backgroundColor: lighten(0.2, newColorFind(item.v_category)) }}
                                />
                            </div>
                        </List.Item>
                    )}
                />
            }
            {searchResult?.backfill && searchResult?.backfill.length > 0 &&
                <>
                    <List
                        dataSource={searchResult?.backfill}
                        loading={isLoading}
                        header='Возможно, вас заинтересуют'
                        locale={{ emptyText: 'Нет данных' }}
                        renderItem={(item) => (
                            <List.Item key={item.id}>
                                <List.Item.Meta
                                    avatar={<Avatar style={{ backgroundColor: lighten(0.2, newColorFind(item.source_channel_title)) }}>{item.source_channel_title[0] + item.source_channel_title[1].toUpperCase()}</Avatar>}
                                    title={<a href="https://ant.design">{item.source_video_title}</a>}
                                    description={item.source_channel_title}
                                />
                                <div>
                                    <Badge
                                        className="site-badge-count-109"
                                        count={item.v_category}
                                        style={{ backgroundColor: lighten(0.2, newColorFind(item.v_category)) }}
                                    />
                                </div>
                            </List.Item>
                        )}
                    />
                </>
            }
            <br />
            <br />
            {requestTime > 0 && <>
                Время выполнения запроса: {requestTime.toFixed(5)} секунды
            </>}
            <br />

            {/* <List
                itemLayout="vertical"
                // size="large"
                size='small'
                dataSource={searchResult?.data}
                renderItem={(item) => (
                    <List.Item
                        key={item.id}
                        actions={[
                            <IconText icon={StarOutlined} text="156" key="list-vertical-star-o" />,
                            <IconText icon={LikeOutlined} text="156" key="list-vertical-like-o" />,
                            <IconText icon={MessageOutlined} text="2" key="list-vertical-message" />,
                        ]}
                        extra={
                            <img
                                width={272}
                                alt="logo"
                                src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
                            />
                        }
                    >
                        <List.Item.Meta
                            avatar={<Avatar>{item.source_channel_title[0]}</Avatar>}
                            title={<a>{item.source_video_title}</a>}
                            description={item.source_channel_title}
                        />
                        {item.v_category} {item.v_channel_type}
                    </List.Item>
                )}
            /> */}

            {/* <Form
                name="basic"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 16 }}
                style={{ maxWidth: 600 }}
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <Form.Item<string>
                    name="cart_id"
                    rules={[
                        { required: true, message: 'Чтобы что-найти, нужно что-то ввести' },
                    ]}
                >
                    <AutoComplete
                        style={{ width: 500 }}
                        onSearch={onSearch}
                        onSelect={onSelect}
                        options={(searchOptions || []).map((d) => ({
                            value: d,
                            title: String(d),
                        }))}
                        notFoundContent={
                            <div style={{ textAlign: 'center' }}>{isSearching ? <Spin size="small" /> : <Typography.Text type='secondary'>Ничего не найдено</Typography.Text>}
                            </div>}
                        value={searchString}
                    >
                        <Input size="large" placeholder="00000000000" />
                    </AutoComplete>
                </Form.Item>

                <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                    <Button type="primary" htmlType="submit" loading={isLoading}>
                        Проверить
                    </Button>
                </Form.Item>
            </Form > */}
        </>
    )
};
