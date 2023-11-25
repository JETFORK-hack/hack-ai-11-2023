import { Avatar, Card, Divider, List, Space, message } from 'antd';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { basePath } from '../../providers/env';
import { useNavigate, useParams } from 'react-router-dom';

const { Meta } = Card;


export interface ICartInfo {
    receipt_id: number;
    item_id: number;
    name: string;
    type: string;
    quantity: number;
    price: number;
    category_noun: string;
    category_url: string | null;
}

interface ICardInfoPredict {
    target?: ICartInfo;
    candidate?: ICartInfo;
    proba?: number;
}

export interface ICardInfoById {
    items: ICartInfo[];
    predict: ICardInfoPredict | null;
}

export const CartInfo = (): JSX.Element => {

    const navigate = useNavigate();
    const { id } = useParams();

    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [cartItems, setCartItems] = useState<ICartInfo[]>([]);


    useEffect(() => {
        console.log('id', id)
        axios.get<ICardInfoById>(basePath + '/api/v1/matching/receipts_by_id', { params: { id } })
            .then((response) => {
                console.log(response.data)
                if (response.data.items.length === 0) {
                    message.error('Корзина не найдена.');
                    navigate('/cart');
                }
                setCartItems(response.data.items)
            })
            .catch(() => {
                message.error('Загрузка не удалась.');
            })
            .finally(() => {
                setIsLoading(false);
            });
    }, [id]);

    return (
        <>
            <br />
            <h1>Элементы корзины №{id}</h1>
            <List
                itemLayout="horizontal"
                dataSource={cartItems}
                renderItem={(item: ICartInfo, index) => (
                    <List.Item>
                        <List.Item.Meta
                            avatar={<Avatar src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`} />}
                            title={item.name}
                            description={item.item_id + ' ' + item.price + '₽'}
                        // description={<Space direction="vertical">
                        //     <div>Артикул {item.item_id}</div>
                        //     <div>{item.price}₽</div>
                        // </Space>}
                        />
                    </List.Item>
                )}
            />
            <br />
            <h1>К этой корзине рекомендуем</h1>
            <Card
                hoverable
                style={{ width: 240 }}
                cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
            >
                <Meta title="Верблюд" description="786.12 ₽" />
            </Card>
        </>
    )
};
