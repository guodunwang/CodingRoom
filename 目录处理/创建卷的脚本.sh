#!/bin/bash  
  
# 定义变量  
VG_NAME="vg1"  
OLD_LV_NAME="lv_apps_clouddb"  
NEW_LV_NAME="lv_he3data" 
MOUNT_POINT="/data/he3pg-data"  
  
# 检查当前挂载情况  
echo "Checking current mount and volume status..."  
sudo lvs  
sudo vgs
sudo lsblk 
  
# 取消挂载（如果已挂载）  
if sudo umount /apps/clouddb; then
    echo "/apps/clouddb has been unmounted."
else
    echo "Failed to unmount /apps/clouddb, please check if it's mounted or used."
    exit 1
fi
  
# 再次检查当前挂载情况  
echo "Checking mount status after unmount..."  
sudo lvs  
sudo vgs
sudo lsblk  
  
# 删除老的LV  
if sudo lvremove -y /dev/${VG_NAME}/${OLD_LV_NAME}; then  
    echo "${OLD_LV_NAME} has been removed."  
else  
    echo "Failed to remove ${OLD_LV_NAME}, please check if it exists or has dependencies."  
    exit 1  
fi  
  
# 创建新的LV  
if sudo lvcreate -y --name ${NEW_LV_NAME} --size 10TB ${VG_NAME}; then  
    echo "${NEW_LV_NAME} has been created."  
else  
    echo "Failed to create ${NEW_LV_NAME}, please check VG size and permissions."  
    exit 1  
fi  
  
# 检查当前挂载情况  
echo "Checking current mount and volume status after creating new LV..."  
sudo lvs  
sudo vgs  
sudo lsblk  
  
# 创建文件系统  
if sudo mkfs.xfs /dev/${VG_NAME}/${NEW_LV_NAME}; then  
    echo "File system has been created on ${NEW_LV_NAME}."  
else  
    echo "Failed to create file system on ${NEW_LV_NAME}, please check for errors."  
    exit 1  
fi  
  
# 获取对应的UUID  
UUID=$(sudo blkid -s UUID -o value /dev/${VG_NAME}/${NEW_LV_NAME})  
echo "UUID of ${NEW_LV_NAME} is: ${UUID}"  
  
# 更新fstab文件  
echo "Updating /etc/fstab..."  
sudo  sed -i '/\/apps/clouddb/s/^/#/' "$FSTAB_FILE" 
if grep -qxF "UUID=${UUID} ${MOUNT_POINT} xfs defaults 0 0" /etc/fstab; then  
    echo "Entry already exists in /etc/fstab, skipping."  
else  
    echo "UUID=${UUID} ${MOUNT_POINT} xfs defaults 0 0" | sudo tee -a /etc/fstab  
    echo "Entry added to /etc/fstab."  
fi  
  
# 创建挂载目录  
sudo mkdir -p ${MOUNT_POINT}  
  
# 调整挂载目录权限  
sudo chmod -R 0755 ${MOUNT_POINT}  
echo "Mount directory ${MOUNT_POINT} created and permissions set."  
  
# 挂载块设备
sudo mount -a  
echo "Mounted ${NEW_LV_NAME} on ${MOUNT_POINT}."  

echo "Script execution completed successfully."

# 安装open-iscsi
#sudo yum install -y open-iscsi 

#sudo service iscsid start 

#echo "open-iscsi successfully."

