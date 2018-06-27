
#pragma once

class ServerCore;
class UnicastServerCore;


// NatNetServer is a simple server for streaming Mocap data.

class DLLCLASS NatNetServer
{
public:

    NatNetServer();
    NatNetServer(int iConnectionType);
    ~NatNetServer();

    int Initialize(char* szLocalAddress);
    int Initialize(char* szLocalAddress, unsigned short CommandPort);
    int Initialize(char* szLocalAddress, unsigned short CommandPort, unsigned short DataPort);
    int Uninitialize();
    void NatNetVersion(unsigned char Version[4]);
    void SetVerbosityLevel(int level);
    int SetErrorMessageCallback(void (*CallbackFunction)(int id, char *szTraceMessage));
    int SetMessageResponseCallback(int(*CallbackFunction)(sPacket* pIncomingMessage, sPacket* pOutgoingResponse, void* pUserData), void* pUserData = 0);
    int SendPacket(sPacket* pPacket);
    int PacketizeFrameOfMocapData(sFrameOfMocapData* pData, sPacket* pOutPacket);
    int PacketizeDataDescriptions(sDataDescriptions* pDescriptions, sPacket* pOutPacket);
    int SendMessageAsynch(char* szMessage);
    int GetSocketInfo(char* szDataIP, int* pDataPort, char* szCommandIP, int* pCommandPort, char* szMulticastIP, int* pMulticastPort);

    static int GetLocalIPAddresses(unsigned long Addresses[], int nMax);
    static int IPAddress_LongToString(unsigned long Address, char *str);

    void SetMulticastAddress(char* szMulticast);

private:

    ServerCore* m_pServerCore;
    int m_iConnectionType;

    //UnicastServerCore* m_pUnicastServerCore;
    //int m_iServerType;
};
