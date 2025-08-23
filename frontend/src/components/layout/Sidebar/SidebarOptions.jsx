import './Sidebar.scss';

export default function SidebarOptions({ name, icon: Icon, path, currentPath }) {
  const handleClick = () => {
    window.history.pushState({}, '', path);
    // Manually trigger a popstate event to notify MainApp.jsx of the change
    const popstateEvent = new PopStateEvent('popstate');
    window.dispatchEvent(popstateEvent);
  };

  // Determine if the current path matches the sidebar option's path for active styling
  const isActive = path === '/' 
    ? currentPath === '/' 
    : currentPath.startsWith(path) && 
      (currentPath.length === path.length || 
       currentPath[path.length] === '/');

  return (
    <button 
      onClick={handleClick}
      className={`sidebar-option ${isActive ? 'sidebar-option--active' : ''}`}
    >
      <Icon className="sidebar-icon" size={24} color="#565D6DFF" />
      <span className="sidebar-name">{name}</span>
    </button>
  );
}
