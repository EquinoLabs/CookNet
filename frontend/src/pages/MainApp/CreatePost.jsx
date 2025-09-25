import Navbar from '../../components/layout/Navbar/Navbar';
import CreatePostForm from '../../components/mainapp/Post/CreatePostForm';
import './MainApp.scss';

const MainApp = () => {
  return (
    <>
    <Navbar />
    <CreatePostForm />
    </>
  );
};

export default MainApp;
