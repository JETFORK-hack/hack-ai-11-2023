import { Typography } from 'antd';
import { basePath } from '../providers/env';
import { useEffect } from 'react';
import axios from 'axios';

const { Link } = Typography;

export const Loading = (): JSX.Element => {


    useEffect(() => {
        axios.get(basePath + '/api/v1/hello-world')
            .then((response) => {
                console.log(response);
            })
    }, []);

    return (
        <>
            <h1>Проверка</h1>
            <div style={{ textAlign: 'right' }}>
                <Link href="https://jetfork.ru/" target="_blank">
                    Все работает
                </Link>
            </div>
            <br />
        </>
    )
};