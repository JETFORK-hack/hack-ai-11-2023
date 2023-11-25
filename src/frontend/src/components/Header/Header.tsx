import jetforkLogo from '../../logo_black_transporent.png';
import { Layout, Menu, Breadcrumb, theme } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';


export default function Header() {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    const navigate = useNavigate();

    const items = [
        // {
        //     key: '1',
        //     label: 'Поиск',
        //     onClick: () => navigate('/cart'),
        // },
        // {
        //     key: '2',
        //     label: 'Проверка товаров',
        //     onClick: () => navigate('/products'),
        // },
    ]


    return (
        <Layout>
            <Layout.Header style={{
                display: 'flex', alignItems: 'center',
                backgroundColor: 'white',
                // background: 'linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%)',
                // mixBlendMode: 'color-burn'
            }}>
                <a href='/' rel="noreferrer" style={{ height: '100%' }}>
                    <img src={jetforkLogo} style={{ height: '100%', paddingRight: 50 }} />
                </a>
                <Menu theme='light' mode="horizontal" items={items}
                    defaultSelectedKeys={['1']} />
            </Layout.Header>
            <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
                <Layout.Content style={{ padding: '0 50px', flex: 1, overflow: 'auto' }}>
                    <Breadcrumb style={{ margin: '16px 0' }}>
                        <Breadcrumb.Item>Hack-ai</Breadcrumb.Item>
                        <Breadcrumb.Item>Международный хакатон</Breadcrumb.Item>
                    </Breadcrumb>
                    <div style={{ background: colorBgContainer, padding: 30, paddingInline: 100 }}>
                        <Outlet />
                    </div>
                </Layout.Content>
                <Layout.Footer style={{ textAlign: 'center' }}>JetFork</Layout.Footer>
            </div>
        </Layout>

    )
}
