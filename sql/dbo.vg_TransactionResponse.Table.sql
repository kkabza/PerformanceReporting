USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_TransactionResponse]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_TransactionResponse](
	[TransactionResponseID] [int] IDENTITY(1,1) NOT NULL,
	[InvoiceKey] [int] NOT NULL,
	[PNRef] [varchar](50) NOT NULL,
	[Result] [int] NOT NULL,
	[CVV2Match] [char](2) NULL,
	[ResponseMessage] [varchar](100) NULL,
	[AuthCode] [varchar](6) NULL,
	[AVSAddr] [char](1) NULL,
	[AVSZip] [char](1) NULL,
	[IAVS] [char](1) NULL,
	[ResponseDate] [datetime] NOT NULL,
	[HostCode] [varchar](10) NULL,
	[RespText] [varchar](20) NULL,
	[SettleDate] [smalldatetime] NULL,
	[BatchID] [int] NULL,
 CONSTRAINT [PK_CreditCard_Response_Tbl] PRIMARY KEY CLUSTERED 
(
	[TransactionResponseID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
