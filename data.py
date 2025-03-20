import pandas as pd
import matplotlib.pyplot as plt
import re

# with open('./data/ice/cm_info_recorder_iceoryx.1.txt') as f_in, open('ice_acc.csv', 'w') as f_out:
#     for line in f_in:
#         f_out.write(re.sub(r'^\[.*?E\] ', '', line))
# exit(0)

plt.rc('font', family='Times New Roman')
def process_data(data):
    data['Size'] = data['Size']/1024
    data['Latency'] = data['Latency']*1000

    grouped = data.groupby('Topic').agg(
        {"Size": "mean", "Latency": ["mean", "std"]})

    grouped.columns = ["Size_Avg", "Latency_Avg", "Latency_Std"]

    grouped = grouped.reset_index()
    return grouped


ice_data = pd.read_csv('ice_acc.csv', names=['Topic', 'Size', 'Latency'])
capilot_data = pd.read_csv('capilot_iacc.csv', names=[
                           'Topic', 'Size', 'Latency'])

ice_topic = ice_data.iloc[:, 0].unique()
capilot_topic = capilot_data.iloc[:, 0].unique()
print("ice topic num: ", len(ice_topic))
print("capilot topic num: ", len(capilot_topic))
diff = list(set(capilot_topic)-set(ice_topic))
print("diff topic num: ", len(diff))

for topic in diff:
    d = capilot_data[capilot_data.iloc[:, 0] == topic]
    ice_data = pd.concat([ice_data, d], ignore_index=True)
print("ice topic num: ", len(ice_data.iloc[:, 0].unique()))

diff = list(set(ice_topic)-set(capilot_topic))
print("diff topic num: ", len(diff))
for topic in diff:
    ice_data = ice_data[ice_data.iloc[:, 0] != topic]

print("ice topic num: ", len(ice_data.iloc[:, 0].unique()))

ice_data = process_data(ice_data)
capilot_data = process_data(capilot_data)


mybins = 15

plt.figure(figsize=(16, 8))

plt.subplot(2, 3, 1)
counts, bins, patches = plt.hist(ice_data['Size_Avg'], bins=mybins,
                                 edgecolor='black', label='iceoryx', color='LightPink')

# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')

plt.title('(a) Data size Distribution(KB) of Iceoryx',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Data size (KB)',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
# plt.xlim(0,1000)
plt.ylim(0,270)

plt.subplot(2, 3, 2)
counts, bins, patches = plt.hist(ice_data['Latency_Avg'], bins=mybins,
                                 edgecolor='black', label='iceoryx', color='LightPink')
# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')

plt.title('(b) Latency Distribution(ms) of Iceoryx',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Latency (ms)',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
plt.ylim(0,210)

plt.subplot(2, 3, 3)
counts, bins, patches = plt.hist(ice_data['Latency_Std'], bins=mybins,
                                 edgecolor='black', label='iceoryx', color='LightPink')
# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')

plt.title('(c) Latency Std Distribution of Iceoryx',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Latency Std',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
plt.ylim(0,110)

plt.subplot(2, 3, 4)
counts, bins, patches = plt.hist(capilot_data['Size_Avg'], bins=mybins,
                                 edgecolor='black', label='capilot', color='LimeGreen')
# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')

plt.title('(d) Data size Distribution(KB) of CAPilot ',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Data size (KB)',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
plt.ylim(0,265)
plt.subplot(2, 3, 5)
counts, bins, patches = plt.hist(capilot_data['Latency_Avg'], bins=mybins,
                                 edgecolor='black', label='capilot', color='LimeGreen')
# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')

plt.title('(e) Latency Distribution(ms) of CAPilot',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Latency (ms)',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
plt.ylim(0,185)

plt.subplot(2, 3, 6)
counts, bins, patches = plt.hist(capilot_data['Latency_Std'], bins=mybins,
                                 edgecolor='black', label='capilot', color='LimeGreen')
# 添加数值标签
for i in range(len(counts)):
    if counts[i] > 0:  # 只显示非零的数值标签
        plt.text((bins[i] + bins[i+1]) / 2, counts[i], f'{int(counts[i])}',
                 ha='center', va='bottom', fontsize=16, color='black')
plt.title('(f) Latency Std Distribution of CAPilot',fontdict={'family': 'Times New Roman', 'size': 16}, y=-0.3)
plt.xlabel('Latency Std (ms)',fontdict={'family': 'Times New Roman', 'size': 16})
plt.ylabel('Frequency',fontdict={'family': 'Times New Roman', 'size': 16})
plt.yticks(fontproperties='Times New Roman', size=16)
plt.xticks(fontproperties='Times New Roman', size=16)
plt.ylim(0,192)
plt.subplots_adjust(left=0.05,right=0.95,top=0.95, bottom=0.1, wspace=0.2,hspace=0.4)
plt.savefig('Fig15.eps', format='eps', dpi=3000)
# plt.savefig('capilot.pdf', format='pdf', dpi=3000)
# plt.savefig('capilot.jpg', format='jpg', dpi=1000)
plt.show()

exit(0)


data = pd.read_csv('capilot_iacc.csv', names=['Topic', 'Size', 'Latency'])
data['Size'] = data['Size']/1024
data['Latency'] = data['Latency']*1000

grouped = data.groupby('Topic').agg(
    {"Size": "mean", "Latency": ["mean", "std"]})

grouped.columns = ["Size_Avg", "Latency_Avg", "Latency_Std"]

grouped = grouped.reset_index()
print("topic num: ", len(grouped))
print("max size: ", grouped['Size_Avg'].max())

plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.hist(grouped['Size_Avg'], bins=10, edgecolor='black')
plt.title('Data size Distribution(KB)')
plt.xlabel('Data size (KB)')
plt.ylabel('Frequency')

plt.subplot(1, 3, 2)
plt.hist(grouped['Latency_Avg'], bins=10, edgecolor='black')
plt.title('Latency Distribution(ms)')
plt.xlabel('Latency (ms)')
plt.ylabel('Frequency')

plt.subplot(1, 3, 3)
plt.hist(grouped['Latency_Std'], bins=10, edgecolor='black')
plt.title('Latency Std Distribution(ms)')
plt.xlabel('Latency Std (ms)')
plt.ylabel('Frequency')

print(grouped)

plt.savefig('capilot.pdf', format='pdf', dpi=500)
plt.show()

# for topic in topics:
#     print(topic)
#     topic_data = data[data.iloc[:, 0] == topic]
#     mean_size = topic_data.iloc[:, 1].mean()
#     mean_latency = topic_data.iloc[:, 2].mean()

#     any_key = input()
